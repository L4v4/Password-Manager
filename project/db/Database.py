from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool

from project.structure.EventHandler import Event, Handler
from project.exceptions.Exceptions import UndefinedBehavior

from typing import List, Optional, NewType


# Use this instead of the `Entry` object to avoid circular imports
_Entry: NewType = NewType("Entry", object)


class DatabaseManager:
    Base: DeclarativeMeta = declarative_base()

    def __init__(self, db_path: Optional[str] = None):
        super().__init__()
        if db_path is not None:
            self.engine: Engine = create_engine(
                f"sqlite:///{db_path}", poolclass=NullPool
            )
            self.session: Session = sessionmaker(bind=self.engine)()
        self.setup_events()
        self.setup_handlers()

    def setup_events(self) -> None:
        self.get_entry_event: Event = Event()
        self.get_all_entries_event: Event = Event()

    def setup_handlers(self):
        self.get_entry_handler: Handler = Handler(self.get_entry)
        self.set_entry_handler: Handler = Handler(self.set_entry)
        self.path_set_handler: Handler = Handler(self.setup_connection)
        self.request_all_entries_handler: Handler = Handler(
            self.request_all_entries
        )
        self.update_entry_handler: Handler = Handler(self.update_entry)
        self.delete_entry_handler: Handler = Handler(self.delete_entry)

    def setup_connection(self, db_path: str):
        if not hasattr(self, "engine"):
            self.engine: Engine = create_engine(f"sqlite:///{db_path}")
            self.session: Session = sessionmaker(bind=self.engine)()
        self.Base.metadata.create_all(self.engine)

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()

    def get_entry(self, **kwargs) -> _Entry:
        self.get_entry_event.invoke(
            self.session.query(Entry).filter_by(**kwargs).first()
        )

    def get_all_entries(self) -> List[_Entry]:
        return self.session.query(Entry).all()

    def request_all_entries(self) -> None:
        self.get_all_entries_event.invoke(self.session.query(Entry).all())

    def set_entry(
        self,
        title: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        check_entry = self.session.query(Entry).filter_by(title=title).first()
        if check_entry is not None:
            raise UndefinedBehavior("Entry already exists.")
        self.session.add(
            Entry(title=title, username=username, password=password)
        )
        self.session.commit()

    def update_entry(
        self,
        title: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        entry: Optional[_Entry] = (
            self.session.query(Entry).filter_by(title=title).first()
        )
        if entry is None:
            raise RuntimeError("Invalid call of update function.")
        entry.username = username
        entry.password = password
        self.session.commit()

    def delete_entry(self, title: str) -> None:
        entry: Optional[_Entry] = (
            self.session.query(Entry).filter_by(title=title).first()
        )
        if entry is None:
            raise RuntimeError("Invalid call of update function.")
        self.session.delete(entry)
        self.session.commit()


from project.db.Models import Entry  # noqa: E402, F401

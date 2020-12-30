from sqlalchemy import Column, Integer, String, Sequence

from project.db.Database import DatabaseManager


class Entry(DatabaseManager.Base):
    __tablename__ = "entries"

    id = Column(Integer, Sequence("entry_id_seq"), primary_key=True)
    title = Column(String(128), unique=True)
    username = Column(String(128))
    password = Column(String(128))

    def __repr__(self):
        return (
            f"<Entry(title='{self.get_title()}',"
            f"username='{self.get_username()}',"
            f"password='{self.get_password()}')>"
        )

    @staticmethod
    def hide_string(s: str):
        return "*" * len(s)

    def get_title(self):
        return self.title

    def get_username(self):
        return self.username

    def get_password(self):
        return self.hide_string(self.password)

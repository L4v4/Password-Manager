import PySimpleGUI as sg

from typing import Any, List, Dict


def LBox(values, key):
    return sg.Listbox(
        values,
        enable_events=True,
        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
        size=(25, 7),
        pad=(0, 0),
        key=key,
    )


class Layout:
    def __init__(self):
        super().__init__()
        self.layout_storage = {
            "FileSelect": [
                [
                    sg.Text("Open File:", size=(10, 1)),
                    sg.In(size=(10, 1), enable_events=True, key="-OPEN-"),
                    sg.FileBrowse(
                        "Browse",
                        size=(8, 1),
                        file_types=(("Encrypted Database", "*.db.enc"),),
                    ),
                ],
                [
                    sg.Text("New File:", size=(10, 1)),
                    sg.In(size=(10, 1), enable_events=True, key="-CREATE-"),
                    sg.FileSaveAs(
                        "New File",
                        size=(8, 1),
                        file_types=(("Encrypted Database", "*.db.enc"),),
                    ),
                ],
            ],
            "PasswordDisplay": [
                [
                    sg.VSeparator(),
                    sg.Column(
                        [
                            [sg.Text("Entry:")],
                            [
                                sg.Text("Title:", size=(15, 1)),
                                sg.InputText(
                                    "",
                                    size=(15, 1),
                                    disabled=True,
                                    key="-TITLE-DISPLAY-",
                                ),
                            ],
                            [
                                sg.Text("Username:", size=(15, 1)),
                                sg.InputText(
                                    "", size=(15, 1), key="-USERNAME-DISPLAY-"
                                ),
                            ],
                            [
                                sg.Text("Password:", size=(15, 1)),
                                sg.InputText(
                                    "", size=(15, 1), key="-PASSWORD-DISPLAY-"
                                ),
                            ],
                            [
                                sg.Button(
                                    "Update",
                                    enable_events=True,
                                    size=(10, 1),
                                    key="-UPDATE-",
                                ),
                                sg.Button(
                                    "Delete",
                                    enable_events=True,
                                    size=(10, 1),
                                    key="-DELETE-",
                                ),
                            ],
                        ]
                    ),
                ],
            ],
            "EntryModifier": [
                [
                    sg.Text("Title (required):", size=(15, 1)),
                    sg.InputText(key="-TITLENAME-"),
                ],
                [
                    sg.Text("Username:", size=(15, 1)),
                    sg.InputText(key="-USERNAME-"),
                ],
                [
                    sg.Text("Password:", size=(15, 1)),
                    sg.InputText(key="-PASSWORD-"),
                ],
                [
                    sg.Submit(),
                    sg.Cancel(),
                ],
            ],
            "NewPassword": [
                [sg.Text("Please enter the password:")],
                [sg.InputText(key="-PASSWORD-")],
                [sg.Submit()],
            ],
            "PasswordRequest": [
                [sg.Text("Please enter the password:")],
                [sg.InputText(key="-NEWPWD-1-")],
                [sg.Text("Please repeat the password:")],
                [sg.InputText(key="-NEWPWD-2-")],
                [sg.Submit()],
            ],
        }

    def get_all_layouts(self) -> List[Dict[str, List[List[Any]]]]:
        """
        Puts all layout into a list.

        Returns:
            A list containing all available layouts.
        """
        return [x for x in self.layout_storage.values()]

    def get_layout(self, layout_name: str) -> List[List[Any]]:
        """
        Gives you the requested layout.

        Args:
            layout_name: The name of the requested layout.

        Returns:
            The requested layout.
        """
        return self.layout_storage[layout_name]

    def add_entries(self, entries: List[str]):
        self.layout_storage["PasswordDisplay"][0].insert(
            0,
            sg.Column(
                [
                    [
                        sg.Text("Title", size=(15, 1)),
                        sg.Button("New", enable_events=True, key="-NEW-"),
                    ],
                    [
                        LBox([e for e in entries], "-TITLE-"),
                    ],
                ],
            ),
        )

    def merge_layouts(self, *layouts):
        return [
            [
                sg.Column(
                    self.layout_storage[layout],
                    key=f"-COL{number}-",
                    visible=(lambda nbr: nbr == 0)(number),
                )
                for number, layout in enumerate(layouts)
            ],
        ]

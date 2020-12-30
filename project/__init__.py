import PySimpleGUI as sg

from project.manager.MainManager import MainManager


def main() -> None:
    sg.theme("DefaultNoMoreNagging")
    main: MainManager = MainManager()
    main.run()

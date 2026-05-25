from PyQt6.QtWidgets import QMessageBox


def display_error(msg: str) -> None:
    QMessageBox.critical(None, "Error", msg)


def display_information(msg: str) -> None:
    QMessageBox.information(None, "Information", msg)

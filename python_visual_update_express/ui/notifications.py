from PyQt6.QtWidgets import QMessageBox

ERROR_TITLE = 'An error has occurred'


def error_notification(text: str, self: any = None) -> None:
    print(text)
    QMessageBox.critical(self, ERROR_TITLE, text)


def warning_notification(text: str, self: any = None) -> None:
    print(text)
    QMessageBox.warning(self, ERROR_TITLE, text)

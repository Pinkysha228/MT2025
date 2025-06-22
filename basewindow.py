from PyQt5.QtWidgets import QWidget, QMessageBox

class BaseWindow(QWidget):
    def __init__(self, header: str) -> None:
        super().__init__()
        self.setWindowTitle(header)
        # self.setWindowIcon("icon.ico")
        with open("style.css", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

    @staticmethod
    def show_modal(header: str, text: str, icon: int = 0) -> int:
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(text)

        match icon:
            case 0:
                msg.setIcon(QMessageBox.Information)
            case 1:
                msg.setIcon(QMessageBox.Warning)
            case 2:
                msg.setIcon(QMessageBox.Critical)
            case 3:
                msg.setIcon(QMessageBox.Question)
            case _:
                raise Exception("Oops, icon number is false")

        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def window(header: str, text: str) -> int:
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(text)

        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = msg.exec_()

        return result

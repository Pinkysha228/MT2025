from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QVBoxLayout
import sys
from basewindow import BaseWindow

money = 0
click = 0

class Clicker(BaseWindow):
    def __init__(self) -> None:
        super().__init__("Expense Tracker")
        self.init_ui()
        self.show()

    def init_ui(self) -> QBoxLayout:
        layout = QVBoxLayout()

        self.money_label = QLabel(f'{money}', self)

        self.add_money = QPushButton(self)
        self.add_money.setIcon(QIcon('bitcoin.png'))
        self.add_money.setIconSize(QSize(200, 200))
        self.add_money.clicked.connect(self.add_money_def)

        layout.addWidget(self.money_label)
        layout.addWidget(self.add_money)

        self.setLayout(layout)

    def add_money_def(self):
        global money, click
        money += 1
        click += 1
        self.money_label.setText(str(money))

app = QApplication(sys.argv)
window = Clicker()
sys.exit(app.exec_())
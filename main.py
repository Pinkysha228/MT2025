from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QVBoxLayout, QMessageBox, \
    QToolButton
from PyQt5.QtCore import QTimer, QPoint
import sys
from basewindow import BaseWindow

money = 0
click = 0
click_cost = 1
cost_upgrade = 50

passive_income = 0
cost_passive_upgrade = 100

class Clicker(BaseWindow):
    def __init__(self) -> None:
        super().__init__("Expense Tracker")
        layout = QVBoxLayout()
        layout.addLayout(self.init_header_layout())
        layout.addLayout(self.init_button())
        layout.addLayout(self.init_footer_layout())
        self.setLayout(layout)
        self.show()

        self.passive_timer = QTimer()
        self.passive_timer.timeout.connect(self.add_passive_income)
        self.passive_timer.start(3000)

        self.random_boost = QTimer()
        self.random_boost.sta #ДОРОБИТИ

    def init_header_layout(self) -> QBoxLayout:
        global click_cost
        layout = QHBoxLayout()

        self.money_label = QLabel(f'Баланс: {money}', self)

        self.cost_click = QLabel(f'Ціна кліку: {click_cost}', self)

        self.boost = QPushButton('Апгрейд', self)
        self.boost.clicked.connect(self.upgrade_menu)

        layout.addWidget(self.money_label)
        layout.addWidget(self.boost)
        layout.addWidget(self.cost_click)
        return layout

    def init_button(self) -> QBoxLayout:
        layout = QVBoxLayout()
        self.add_money = QPushButton(self)
        self.add_money.setIcon(QIcon('bitcoin.png'))
        self.add_money.setIconSize(QSize(200, 200))
        self.add_money.clicked.connect(self.add_money_def)

        layout.addWidget(self.add_money)
        return layout

    def init_footer_layout(self) -> QBoxLayout:
        layout = QVBoxLayout()
        self.passive_label = QLabel(f'Пасивний дохід: {passive_income}', self)
        self.passive_upgrade = QPushButton(f'Купити пасивний дохід', self)
        self.passive_upgrade.clicked.connect(self.upgrade_passive_income)

        layout.addWidget(self.passive_label)
        layout.addWidget(self.passive_upgrade)

        return layout

    def add_money_def(self):
        global money, click
        money = click_cost * 1 + money
        click += 1
        self.money_label.setText(f'Баланс: {str(money)}')

        original_pos = self.add_money.pos()
        offsets = [QPoint(5, 0), QPoint(-5, 0), QPoint(0, 5), QPoint(0, -5)]

        def shake():
            if offsets:
                self.add_money.move(original_pos + offsets.pop(0))
                QTimer.singleShot(50, shake)
            else:
                self.add_money.move(original_pos)

        shake()

    def upgrade_menu(self):
        global click_cost, cost_upgrade, money
        clicked = BaseWindow.window('Апгрейд', f'Ціна апгрейду: {cost_upgrade}')
        if clicked == QMessageBox.Yes:
            if money >= cost_upgrade:
                click_cost += 0.5
                money -= cost_upgrade
                cost_upgrade *= 2
                self.money_label.setText(f'Баланс: {str(money)}')

    def upgrade_passive_income(self):
        global money, passive_income, cost_passive_upgrade
        clicked = BaseWindow.window('Пасивний апгрейд', f'Ціна пасивного апгрейду: {cost_passive_upgrade}')
        if clicked == QMessageBox.Yes:
            if money >= cost_passive_upgrade:
                money -= cost_passive_upgrade
                passive_income += 1
                cost_passive_upgrade *= 2
                self.money_label.setText(f'Баланс: {money}')
                self.passive_label.setText(f'Пасивний дохід: {passive_income}')
                self.passive_upgrade.setText(f'Купити пасивний дохід')

    def add_passive_income(self):
        global money, passive_income
        if passive_income > 0:
            money += passive_income
            self.money_label.setText(f'Баланс: {money}')

    def boost_money(self):
        global money
        money += 10
        self.money_label.setText(f'Баланс: {money}')
        

app = QApplication(sys.argv)
window = Clicker()
sys.exit(app.exec_())

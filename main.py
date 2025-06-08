from PyQt5.QtCore import QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QVBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtCore import QTimer, QPoint
import sys
from basewindow import BaseWindow
import random
import json

money = 0
click = 0
click_cost = 1
cost_upgrade = 50

passive_income = 0
cost_passive_upgrade = 100

username = None
password = None


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
        self.random_boost.timeout.connect(self.boost_money)
        self.random_boost.start(random.randint(10000, 60000))

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
        layout = QHBoxLayout()
        self.passive_label = QLabel(f'Пасивний дохід: {passive_income}', self)
        self.passive_upgrade = QPushButton(f'Пасивний дохід', self)
        self.passive_upgrade.clicked.connect(self.upgrade_passive_income)

        layout.addWidget(self.passive_label)
        layout.addWidget(self.passive_upgrade)

        return layout

    def add_money_def(self):
        global money, click
        money = click_cost * 1 + money
        click += 1
        self.money_label.setText(f'Баланс: {str(money)}')

        def animate_click(btn):
            orig_size = btn.size()
            orig_pos = btn.pos()

            scale = 0.90
            new_width = int(orig_size.width() * scale)
            new_height = int(orig_size.height() * scale)
            delta_w = (orig_size.width() - new_width) // 2
            delta_h = (orig_size.height() - new_height) // 2
            shrink_pos = orig_pos + QPoint(delta_w, delta_h)

            size_anim = QPropertyAnimation(btn, b"size")
            size_anim.setDuration(150)
            size_anim.setKeyValueAt(0, orig_size)
            size_anim.setKeyValueAt(0.5, QSize(new_width, new_height))
            size_anim.setKeyValueAt(1, orig_size)
            size_anim.setEasingCurve(QEasingCurve.InOutQuad)

            pos_anim = QPropertyAnimation(btn, b"pos")
            pos_anim.setDuration(150)
            pos_anim.setKeyValueAt(0, orig_pos)
            pos_anim.setKeyValueAt(0.5, shrink_pos)
            pos_anim.setKeyValueAt(1, orig_pos)
            pos_anim.setEasingCurve(QEasingCurve.InOutQuad)

            size_anim.start()
            pos_anim.start()

            btn._size_anim = size_anim
            btn._pos_anim = pos_anim

        animate_click(self.add_money)

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
                self.passive_upgrade.setText(f'Пасивний дохід')

    def add_passive_income(self):
        global money, passive_income
        if passive_income > 0:
            money += passive_income
            self.money_label.setText(f'Баланс: {money}')

    def boost_money(self):
        global money
        add_money = random.randint(1, 30)
        money += add_money
        self.money_label.setText(f'Бонус! Зараховано: {add_money}')

    def closeEvent(self, event):
        global money, click, click_cost, cost_upgrade, passive_income, cost_passive_upgrade, username, password
        info = {
            'login': username,
            'password': password,
            'money': money,
            'click': click,
            'click_cost': click_cost,
            'cost_upgrade': cost_upgrade,
            'passive_income': passive_income,
            'cost_passive_upgrade': cost_passive_upgrade
        }

        with open(f'users/{username}.json', 'w', encoding='utf-8') as file:
            json.dump(info, file, ensure_ascii=False, indent=4)

        event.accept() # доробити



class RegisterWindow(BaseWindow):
    def __init__(self) -> None:
        super().__init__('Login')

        self.window = None

        layout = QVBoxLayout()
        layout.addLayout(self.header_layout())
        layout.addLayout(self.footer_layout())
        self.setLayout(layout)
        self.show()

    def header_layout(self) -> QBoxLayout:
        layout = QVBoxLayout()
        self.login = QLineEdit()
        self.login.setPlaceholderText("Ім'я користувача")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль користувача")

        layout.addWidget(self.login)
        layout.addWidget(self.password)

        return layout

    def footer_layout(self) -> QBoxLayout:
        layout = QHBoxLayout()
        self.login_btn = QPushButton('Війти')
        self.login_btn.clicked.connect(self.login_clicked)

        self.register_btn = QPushButton('Зареєструватися')
        self.register_btn.clicked.connect(self.register)

        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        return layout

    def register(self):
        global money, click, click_cost, cost_upgrade, passive_income, cost_passive_upgrade, username, password
        info = {
            'login': self.login.text(),
            'password': self.password.text(),
            'money': money,
            'click': click,
            'click_cost': click_cost,
            'cost_upgrade': cost_upgrade,
            'passive_income': passive_income,
            'cost_passive_upgrade': cost_passive_upgrade
        }

        username = info['login']
        password = info['password']

        with open(f'users/{self.login.text()}.json', 'w', encoding='utf-8') as file:
            json.dump(info, file, ensure_ascii=False, indent=4)

    def login_clicked(self):
        login = self.login.text()
        password = self.password.text()
        try:
            with open(f'users/{login}.json', 'r', encoding='utf-8') as file:
                print('file found')
                data = json.load(file)
        except FileNotFoundError:
            BaseWindow.show_modal('Помилка', 'Неправильний логін або пароль', 2)

        if password == data['password']: # вікно відкривається на 1 кадр
            print('password')
            self.window = Clicker()




app = QApplication(sys.argv)
window = RegisterWindow()
sys.exit(app.exec_())

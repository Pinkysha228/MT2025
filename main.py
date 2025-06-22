from PyQt5.QtCore import QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QVBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtCore import QTimer, QPoint
import sys, os
from basewindow import BaseWindow
import random
import json
import requests

money = 0
click = 0
click_cost = float(0.01)
cost_upgrade = float(0.5)

passive_income = 0
cost_passive_upgrade = float(0.0001)

username = None


class Clicker(BaseWindow):
    def __init__(self) -> None:
        super().__init__("Clicker")
        self.load_savefile()
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
        self.random_boost.start(random.randint(10000, 10000))


    def load_savefile(self):
        global money, click, click_cost, cost_upgrade, passive_income, cost_passive_upgrade, username

        with open(f'users/{username}.json', 'r') as f:
            data = json.load(f)
        print(data)
        money = round(data['money'], 4)
        click = data['click']
        click_cost = round(data['click_cost'], 4)
        cost_upgrade = data['cost_upgrade']
        passive_income = data['passive_income']
        cost_passive_upgrade = data['cost_passive_upgrade']



    def init_header_layout(self) -> QBoxLayout:
        global click_cost
        layout = QHBoxLayout()

        self.money_label = QLabel(f'Баланс: {money}', self)

        self.cost_click = QLabel(f'Ціна кліку: {click_cost}', self)

        self.boost = QPushButton('Апгрейд', self)
        self.boost.clicked.connect(self.upgrade_menu)

        layout.addWidget(self.money_label)
        layout.addWidget(self.cost_click)
        layout.addWidget(self.boost)
        return layout

    def init_button(self) -> QBoxLayout:
        layout = QVBoxLayout()
        self.add_money = QPushButton(self)
        self.add_money.setObjectName("main_button")
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
        self.money_label.setText(f'Баланс: {round(money, 4)}')

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
        clicked = BaseWindow.window('Апгрейд', f'Ціна апгрейду: {cost_upgrade}') # <- почему то не синхронно с файлом сохранения
        if clicked == QMessageBox.Yes:
            if money >= cost_upgrade:
                click_cost += 0.05
                money -= cost_upgrade
                cost_upgrade *= 2
                self.money_label.setText(f'Баланс: {round(money, 4)}')
                self.cost_click.setText(f'Ціна кліку: {round(click_cost, 4)}')
                self.boost.setText('Апгрейд')

    def upgrade_passive_income(self):
        global money, passive_income, cost_passive_upgrade
        clicked = BaseWindow.window('Пасивний апгрейд', f'Ціна пасивного апгрейду: {cost_passive_upgrade}')
        if clicked == QMessageBox.Yes:
            if money >= cost_passive_upgrade:
                money = round(money - cost_passive_upgrade, 4)
                passive_income += 0.01
                cost_passive_upgrade *= 2
                self.money_label.setText(f'Баланс: {round(money, 4)}')
                self.passive_label.setText(f'Пасивний дохід: {round(passive_income, 4)}')
                self.passive_upgrade.setText(f'Пасивний дохід')

    def add_passive_income(self):
        global money, passive_income
        if passive_income > 0:
            money += passive_income
            self.money_label.setText(f'Баланс: {round(money, 4)}')

    def boost_money(self):
        global money
        coef = round(click_cost * 0.05 + 0.005, 4)
        print(coef)
        add_money = random.uniform(coef*0.1, coef*0.5)
        money += add_money
        self.money_label.setText(f'Бонус! Зараховано: {round(add_money, 4)}')

    def closeEvent(self, event):
        global money, click, click_cost, cost_upgrade, passive_income, cost_passive_upgrade, username, password
        info = {
            'money': money,
            'click': click,
            'click_cost': click_cost,
            'cost_upgrade': cost_upgrade,
            'passive_income': passive_income,
            'cost_passive_upgrade': cost_passive_upgrade
        }

        with open(f'users/{username}.json', 'w', encoding='utf-8') as file:
            json.dump(info, file, ensure_ascii=False, indent=4)

        event.accept()


API_URL = "http://127.0.0.1:8000"

class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__("Clicker")
        layout = QVBoxLayout()
        # login
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        # password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        # buttons
        self.login_button = QPushButton("Увійти")
        self.register_button = QPushButton("Реєстрація")
        layout.addWidget(QLabel("Логін: "))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль: "))
        layout.addWidget(self.password_input)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.show()
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        self.login_window = None
    def login(self):
        self.send_request("/login")
    def register(self):
        self.send_request("/register")
    def send_request(self, endpoint):
        global username, money, click, click_cost, cost_upgrade, passive_income, cost_passive_upgrade, username, password
        username = self.login_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            BaseWindow.show_modal('Помилка', 'Заповніть всі поля', 2)
            return
        try:
            response = requests.post(
                API_URL + endpoint,
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                message = response.json().get("message", "Успішно")
                QMessageBox.information(self, "Успіх", message)
                self.close()
                if not os.path.isfile(f'users/{username}.json'):
                    info = {
                        'money': money,
                        'click': click,
                        'click_cost': click_cost,
                        'cost_upgrade': cost_upgrade,
                        'passive_income': passive_income,
                        'cost_passive_upgrade': cost_passive_upgrade
                    }

                    with open(f'users/{username}.json', 'w', encoding='utf-8') as file:
                        json.dump(info, file, ensure_ascii=False, indent=4)

                if self.login_window is None:
                    self.login_window = Clicker()
                self.login_window.show()
            else:
                error = response.json().get("detail", "Помилка")
                QMessageBox.critical(self, "Помилка", error)
        except requests.exceptions.ConnectionError:
                QMessageBox.critical(self, "Помилка", "Сервер недоступний")


app = QApplication(sys.argv)
window = LoginWindow()
sys.exit(app.exec_())
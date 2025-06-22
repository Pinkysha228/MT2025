import sys
import requests
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QMainWindow, QWidget, QLabel, QMessageBox
API_URL = "http://127.0.0.1:8000"
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()
        #login
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Login")
        #password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        #buttons
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
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
    def login(self):
        self.send_request("/login")
    def register(self):
        self.send_request("/register")
    def send_request(self, endpoint):
        username = self.login_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Усі поля обов’язкові")
            return
        try:
            response = requests.post(
                API_URL + endpoint,
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                message = response.json().get("message", "Успішно")
                QMessageBox.information(self, "Успіх", message)
                self.close() # Закриває вікно після успіху
            else:
                error = response.json().get("detail", "Помилка")
                QMessageBox.critical(self, "Помилка", error)
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Помилка", "Сервер недоступний")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("meow")
        self.setGeometry(750, 100, 600, 600)
        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        self.button = QPushButton("Вхід", self)
        self.button.setFixedSize(50, 50)
        self.button.clicked.connect(self.open_login_window)
        main_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)
        self.login_window = None
    def open_login_window(self):
        if self.login_window is None:
            self.login_window = LoginWindow()
        self.login_window.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


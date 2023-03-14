from PyQt5.QtWidgets import QMainWindow, QLabel,\
    QLineEdit, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import pandas as pd
import PricerGUI
import PopupGUI
from datetime import datetime


class LoginWindow(QMainWindow):

    def __init__(self, prediction_model):
        super().__init__()

        self.list = pd.read_csv('username_password.csv')

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Login')

        self.label = QLabel()

        layout = QVBoxLayout()
        layout.setContentsMargins(70, 70, 70, 70)
        layout.setSpacing(7)

        # Create title
        title_hold = QHBoxLayout()
        title_hold.setContentsMargins(70, 20, 70, 20)
        title_hold.setAlignment(Qt.AlignHCenter)

        self.title = QLabel("Welcome to Diamond Pricer!")

        title_hold.addWidget(self.title)
        layout.addLayout(title_hold)

        # Create labels and fields for username and password
        hbox1 = QHBoxLayout()

        vbox_username = QVBoxLayout()
        vbox_username.setContentsMargins(50, 0, 50, 0)
        vbox_username.addWidget(QLabel("User Name"))
        self.username_field = QLineEdit()
        vbox_username.addWidget(self.username_field)

        vbox_password = QVBoxLayout()
        vbox_password.setContentsMargins(50, 0, 50, 0)
        vbox_password.addWidget(QLabel("Password"))
        self.password_field = QLineEdit()
        vbox_password.addWidget(self.password_field)

        hbox1.addLayout(vbox_username)
        hbox1.addLayout(vbox_password)

        layout.addLayout(hbox1)

        # Create confirmation button
        button_hold = QHBoxLayout()
        button_hold.setContentsMargins(70, 50, 70, 50)
        submit_button = QPushButton("Submit")
        button_hold.addWidget(submit_button)
        layout.addLayout(button_hold)

        submit_button.clicked.connect(self.submit_button_pushed)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.model = prediction_model

        # Empty attributes to hold handles for other windows
        self.pricer = None
        self.popup = None

    def validate_password(self, username, password):
        """Check if username and password have match, and whether user is admind"""
        is_user = False
        is_admin = False

        for i in range(len(self.list)):
            if username == str(self.list['username'][i]):
                if password == str(self.list['password'][i]):
                    is_user = True
                    if self.list['admin'][i] == 1:
                        is_admin = True

        return is_user, is_admin

    def submit_button_pushed(self):
        """Slot catches signal from pressing submit button, validates username and password"""
        # print("The submit button was pushed.")

        username = self.username_field.text()
        password = self.password_field.text()

        is_user, is_admin = self.validate_password(username, password)

        if is_user:
            print("User accepted")
            self.pricer = PricerGUI.PricerWindow(is_admin, self.model)
            self.pricer.show()
            self.close()
        else:
            print("User not accepted")

            self.popup = PopupGUI.PopupWindow(self,
                                              "BAD ENTRY",
                                              "Invalid Credentials",
                                              "Username and/or password not recognized")
            self.hide()
            self.popup.show()

            with open('bad_user_password_record.txt', 'a') as file:
                file.write("\"{}\",\"{}\",{}\n".format(username, password, datetime.now()))

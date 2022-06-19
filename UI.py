import sys
import PyQt5
from PyQt5.QtWidgets import *

from UserFunctions import login, register


class LoginWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        self.formLayout = QFormLayout()

        self.email = QLineEdit()
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.addRow("Email:", self.email)
        self.formLayout.addRow("Password:", self.passwd)

        # Add a button box
        btnBox = QDialogButtonBox()

        self.login_btn = QPushButton("OK")
        self.login_btn.clicked.connect(self.LoginClicked)
        btnBox.addButton(self.login_btn, QDialogButtonBox.AcceptRole)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.CancelClicked)
        btnBox.addButton(self.cancel_btn, QDialogButtonBox.RejectRole)

        # Set the layout on the dialog
        self.dlgLayout.addLayout(self.formLayout)
        self.dlgLayout.addWidget(btnBox)
        self.setLayout(self.dlgLayout)

    def LoginClicked(self):
        pass

    def CancelClicked(self):
        app.quit()


class RegisterWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        self.formLayout = QFormLayout()

        self.email = QLineEdit()
        self.fullname = QLineEdit()
        self.birthday = QDateEdit()
        self.phonenumber = QLineEdit()
        self.address = QLineEdit()
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwd_again = QLineEdit()
        self.passwd_again.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.addRow("Email:", self.email)
        self.formLayout.addRow("Fullname:", self.fullname)
        self.formLayout.addRow("Birthday:", self.birthday)
        self.formLayout.addRow("Phone:", self.phonenumber)
        self.formLayout.addRow("Address:", self.address)
        self.formLayout.addRow("Password:", self.passwd)
        self.formLayout.addRow("Password again:", self.passwd_again)

        # Add a button box
        btnBox = QDialogButtonBox()

        self.login_btn = QPushButton("OK")
        self.login_btn.clicked.connect(self.RegisterClicked)
        btnBox.addButton(self.login_btn, QDialogButtonBox.AcceptRole)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.CancelClicked)
        btnBox.addButton(self.cancel_btn, QDialogButtonBox.RejectRole)

        # Set the layout on the dialog
        self.dlgLayout.addLayout(self.formLayout)
        self.dlgLayout.addWidget(btnBox)
        self.setLayout(self.dlgLayout)

    def RegisterClicked(self):
        if self.passwd.text != self.passwd_again.text:
            QMessageBox.about(self, "Error", "Re-entered password is incorrect")
            self.passwd.text = ""
            self.passwd_again.text = ""
        else:
            reg = register(self.email.text, self.passwd.text, self.fullname.text, self.birthday.text, self.phonenumber.text, self.address.text)
            if reg == False:
                QMessageBox.about(self, "Error", "Register unsuccessful (Unexpected error occured)!!!")
            else:
                QMessageBox.about(self, "Success", "Successfully register")

    def CancelClicked(self):
        app.quit()


class FirstWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Darkhold")
        self.resize(400, 300)
        self.layout = QVBoxLayout()

        self.login = LoginWindow()
        self.register = RegisterWindow()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.login, "Login")
        self.tabs.addTab(self.register, "Register")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.first = FirstWindow()
        self.first.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    execute = MainWindow()
    sys.exit(app.exec_())

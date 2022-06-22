import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from UserFunctions import *
from globalobject import GlobalObject


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

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.LoginClicked)
        btnBox.addButton(self.login_btn, QDialogButtonBox.AcceptRole)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.CancelClicked)
        btnBox.addButton(self.cancel_btn, QDialogButtonBox.RejectRole)

        # Set the layout on the dialog
        self.dlgLayout.addLayout(self.formLayout)
        self.dlgLayout.addWidget(btnBox)
        self.setLayout(self.dlgLayout)

    @QtCore.pyqtSlot()
    def LoginClicked(self):
        if self.email.text() == "" or self.passwd.text() == "":
            QMessageBox.warning(self, "Login", "Empty email or password entered", QMessageBox.Ok)
        else:
            log, err = login(self.email.text(), self.passwd.text())
            if log:
                QMessageBox.about(self, "Login", "Successfully Login")
                GlobalObject().dispatchEvent("second")
            else:
                QMessageBox.warning(self, "Login", err, QMessageBox.Ok)

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
        self.passwd_confirm = QLineEdit()
        self.passwd_confirm.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.addRow("Email:", self.email)
        self.formLayout.addRow("Fullname:", self.fullname)
        self.formLayout.addRow("Birthday:", self.birthday)
        self.formLayout.addRow("Phone:", self.phonenumber)
        self.formLayout.addRow("Address:", self.address)
        self.formLayout.addRow("Password:", self.passwd)
        self.formLayout.addRow("Confirm Password:", self.passwd_confirm)

        # Add a button box
        btnBox = QDialogButtonBox()

        self.reg_btn = QPushButton("OK")
        self.reg_btn.clicked.connect(self.RegisterClicked)
        btnBox.addButton(self.reg_btn, QDialogButtonBox.AcceptRole)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.CancelClicked)
        btnBox.addButton(self.cancel_btn, QDialogButtonBox.RejectRole)

        # Set the layout on the dialog
        self.dlgLayout.addLayout(self.formLayout)
        self.dlgLayout.addWidget(btnBox)
        self.setLayout(self.dlgLayout)

    def RegisterClicked(self):
        if self.passwd.text() != self.passwd_confirm.text():
            QMessageBox.about(self, "Error", "Confirm password is mismatch")
            self.passwd_confirm.setText("")
        else:
            reg = register(self.email.text(), self.passwd.text(), self.fullname.text(), self.birthday.text(), self.phonenumber.text(), self.address.text())
            if not reg:
                QMessageBox.warning(self, "Register", "Register unsuccessful (Unexpected error occured)!!!", QMessageBox.Ok)
            else:
                QMessageBox.about(self, "Register", "Successfully register")
                self.ClearInputs()

    def CancelClicked(self):
        app.quit()

    def ClearInputs(self):
        self.email.setText("")
        self.fullname.setText("")
        self.phonenumber.setText("")
        self.address.setText("")
        self.passwd.setText("")
        self.passwd_confirm.setText("")


class AppWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.dlglayout = QVBoxLayout()

        self.lb = QLabel("Nothing here", self)

        self.dlglayout.addWidget(self.lb)
        self.setLayout(self.dlglayout)



class EditProfileWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.dlgLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.email = QLineEdit()
        self.fullname = QLineEdit()
        self.birthday = QDateEdit()
        self.phonenumber = QLineEdit()
        self.address = QLineEdit()
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwd_confirm = QLineEdit()
        self.passwd_confirm.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.addRow("Email:", self.email)
        self.formLayout.addRow("Fullname:", self.fullname)
        self.formLayout.addRow("Birthday:", self.birthday)
        self.formLayout.addRow("Phone:", self.phonenumber)
        self.formLayout.addRow("Address:", self.address)
        self.formLayout.addRow("Password:", self.passwd)
        self.formLayout.addRow("Confirm Password:", self.passwd_confirm)

        # Add a button box
        btnBox = QDialogButtonBox()

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.SaveEditClicked)
        btnBox.addButton(self.save_btn, QDialogButtonBox.AcceptRole)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.ClearClicked)
        btnBox.addButton(self.clear_btn, QDialogButtonBox.RejectRole)

        # Set the layout on the dialog
        self.dlgLayout.addLayout(self.formLayout)
        self.dlgLayout.addWidget(btnBox)
        self.setLayout(self.dlgLayout)

    def SaveEditClicked(self):
        if self.passwd.text() != self.passwd_confirm.text():
            QMessageBox.about(self, "Error", "Confirm password is mismatch")
            self.passwd_confirm.setText("")
        else:
            reg, resp = edit_profile(self.email.text(), self.passwd.text(), self.fullname.text(), self.birthday.text(), self.phonenumber.text(), self.address.text())
            if not reg:
                QMessageBox.warning(self, "Edit Profile", resp, QMessageBox.Ok)
            else:
                QMessageBox.about(self, "Edit Profile", "Successfully save changes")

    def ClearClicked(self):
        self.email.setText("")
        self.fullname.setText("")
        self.phonenumber.setText("")
        self.address.setText("")
        self.passwd.setText("")
        self.passwd_confirm.setText("")


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


class SecondWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Darkhold")
        self.resize(400, 300)
        self.layout = QVBoxLayout()

        self.appl = AppWindow()
        self.edit_profile = EditProfileWindow()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.appl, "Application")
        self.tabs.addTab(self.edit_profile, "Edit Profile")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.first_window = FirstWindow()
        self.second_window = SecondWindow()

        GlobalObject().addEventListener("second", self.OpenSecondWindow)

        self.first_window.show()

    @QtCore.pyqtSlot()
    def OpenSecondWindow(self):
        if self.first_window.isVisible():
            self.first_window.close()
        self.second_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    execute = MainWindow()
    sys.exit(app.exec_())

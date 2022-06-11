import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QStackedWidget
from PyQt5.uic import loadUi

class LoginWindow(QDialog):
    def __init__(self) -> None:
        super(LoginWindow, self).__init__()
        loadUi("login_ui.ui", self)
        self.setWindowTitle("Application")
        self.LoginBtn.clicked.connect(self.LoginClicked)
        self.OpenRegister.clicked.connect(self.OpenRegisterClicked)

    def LoginClicked(self):
        inputmail = self.inputmain.text()
        inputpasswd = self.inputpasswd.text()

    def OpenRegisterClicked(self):
        reg = RegisterWindow()
        widgets.addWidget(reg)
        widgets.setCurrentIndex(widgets.currentIndex() + 1)
        print(widgets.currentIndex())

class RegisterWindow(QDialog):
    def __init__(self) -> None:
        super(RegisterWindow, self).__init__()
        loadUi("register_ui.ui", self)
        self.RegisterBtn.clicked.connect(self.RegisterClicked)
        self.CancelBtn.clicked.connect(self.CancelClicked)
        
    def RegisterClicked(self):
        pass

    def CancelClicked(self):
        mainwindow = LoginWindow()
        widgets.addWidget(mainwindow)
        widgets.setCurrentIndex(widgets.currentIndex() + 1)
        print(widgets.currentIndex())


# Initiate application
app = QApplication(sys.argv)
mainwindow = LoginWindow()

widgets = QStackedWidget()
widgets.addWidget(mainwindow)
widgets.show()

app.exec_()
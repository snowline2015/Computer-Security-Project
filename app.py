import sys
import os
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
                GlobalObject().dispatchEvent("second")
                GlobalObject().addUser(self.email.text())
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


class EncryptFileWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.vblayout = QVBoxLayout()

        self.lb = QLabel("Choose a file for encyption")
        self.send_email = QLineEdit()
        self.send_email.setPlaceholderText("Enter email")
        self.file_btn = QPushButton("Choose file")
        self.file_btn.clicked.connect(self.EncryptFile)
        self.stat = QLabel("")

        self.vblayout.addWidget(self.lb)
        self.vblayout.addWidget(self.send_email)
        self.vblayout.addWidget(self.file_btn)
        self.vblayout.addWidget(self.stat)
        self.setLayout(self.vblayout)

    def EncryptFile(self):
        if self.send_email.text() == "":
            QMessageBox.warning(self, "Encrypt file", "Target email is empty!!!", QMessageBox.Ok)
        elif not check_user_exist(self.send_email.text()):
            QMessageBox.warning(self, "Encrypt file", "Email not exist!!!", QMessageBox.Ok)
        elif not check_exist_key(self.send_email.text()):
            QMessageBox.warning(self, "Encrypt file", "Keys are empty!!!", QMessageBox.Ok)
        else:
            file , chk = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)")
            if chk:
                c = file_encrypt(self.send_email.text(), file)
                if c:
                    QMessageBox.about(self, "Encrypt File", "File Encrypt Successfully")
                    self.stat.setText("Your file is encypted.\nCheck your current directory: " + os.getcwd())
                else:
                    QMessageBox.warning(self, "Encypt File", "Unexpected error occurred!!!", QMessageBox.Ok)


class DecryptFileWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.vblayout = QVBoxLayout()

        self.lb = QLabel("Choose a file for decyption")
        self.file_btn = QPushButton("Choose file")
        self.file_btn.clicked.connect(self.DecryptFile)
        self.stat = QLabel("")

        self.vblayout.addWidget(self.lb)
        self.vblayout.addWidget(self.file_btn)
        self.vblayout.addWidget(self.stat)
        self.setLayout(self.vblayout)

    def DecryptFile(self):
        if not check_exist_key(GlobalObject().getUser()):
            QMessageBox.warning(self, "Decrypt file", "Keys are empty!!!", QMessageBox.Ok)
        else:
            file , chk = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)")
            if chk:
                c = file_decrypt(GlobalObject().getUser(), file)
                if c:
                    QMessageBox.about(self, "Decrypt File", "File Decrypt Successfully")
                    self.stat.setText("Your file is decypted.\nCheck your current directory: " + os.getcwd())
                else:
                    QMessageBox.warning(self, "Decypt File", "Unexpected error occurred!!!", QMessageBox.Ok)


class SignFileWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.vblayout = QVBoxLayout()

        self.lb = QLabel("Choose a file to sign")
        self.file_btn = QPushButton("Choose file")
        self.file_btn.clicked.connect(self.GetFilePath)
        self.stat = QLabel("")

        self.vblayout.addWidget(self.lb)
        self.vblayout.addWidget(self.file_btn)
        self.vblayout.addWidget(self.stat)
        self.setLayout(self.vblayout)

    def GetFilePath(self):
        if not check_exist_key(GlobalObject().getUser()):
            QMessageBox.warning(self, "Sign file", "Keys are empty!!!", QMessageBox.Ok)
        else:
            file , chk = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)")
            if chk:
                c = digital_signature(GlobalObject().getUser(), file)
                if c:
                    QMessageBox.about(self, "Sign File", "File Sign Successfully")
                    self.stat.setText("Check out for signature file: " + os.getcwd())
                else:
                    QMessageBox.warning(self, "Sign File", "Unexpected error occurred!!!", QMessageBox.Ok)


class VerifyFileSignWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.vblayout = QVBoxLayout()

        self.lb = QLabel("Choose a file for sign verification")
        self.file_btn = QPushButton("Choose file")
        self.file_btn.clicked.connect(self.GetFilePath)
        self.stat = QLabel("")

        self.vblayout.addWidget(self.lb)
        self.vblayout.addWidget(self.file_btn)
        self.vblayout.addWidget(self.stat)
        self.setLayout(self.vblayout)

    def GetFilePath(self):
        if not check_exist_key(GlobalObject().getUser()):
            QMessageBox.warning(self, "Verify sign", "Keys are empty!!!", QMessageBox.Ok)
        else:
            file , chk = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "Signature Files (*.sig)")
            if chk:
                c, signed_user = digital_signature_verification(file)
                if c:
                    QMessageBox.about(self, "Verify File Sign", "Valid Signature")
                    self.stat.setText("Valid Signature.\nFile was signed by " + signed_user)
                else:
                    QMessageBox.warning(self, "Verify File Sign", "Cannot verify signature", QMessageBox.Ok)
                    self.stat.setText("Verify failed")


class GenerateKeysWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.vblayout = QVBoxLayout()

        self.gen_btn = QPushButton("Generate Keys")
        self.gen_btn.clicked.connect(self.GenerateKeys)
        self.stat = QLabel("")

        self.vblayout.addWidget(self.gen_btn)
        self.vblayout.addWidget(self.stat)
        self.setLayout(self.vblayout)

    def GenerateKeys(self):
        if check_exist_key(GlobalObject().getUser()):
            QMessageBox.warning(self, "Generate Keys", "Keys existed!!!", QMessageBox.Ok)
        else:
            c = generate_key(GlobalObject().getUser())
            if c:
                QMessageBox.about(self, "Generate Keys", "Keys generated successfully")
                self.stat.setText("Keys generated successfully.")
            else:
                QMessageBox.warning(self, "Generate Keys", "An unexpected error occurred!!!", QMessageBox.Ok)
                self.stat.setText("Error")


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
                QMessageBox.about(self, "Edit Profile", "Successfully save changes.")

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
        self.setMinimumSize(600, 400)
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
        self.setMinimumSize(600, 400)

        self.vblayout = QVBoxLayout()
        menubar = QMenuBar()

        options = menubar.addMenu("Options")
        options.addAction("Generate asymmetric keys")
        options.addAction("Encrypt File")
        options.addAction("Decrypt File")
        options.addAction("Sign File")
        options.addAction("Verify Sign")
        options.addAction("Edit Profile")

        options.triggered[QAction].connect(self.NavigateOptions)
        
        self.edit_profile = EditProfileWindow()
        self.encr = EncryptFileWindow()
        self.decr = DecryptFileWindow()
        self.sign = SignFileWindow()
        self.verify = VerifyFileSignWindow()
        self.gen_keys = GenerateKeysWindow()

        self.vblayout.addWidget(menubar)
        self.setLayout(self.vblayout)

    def NavigateOptions(self, opt):
        if opt.text() == "Encrypt File":
            self.OpenEncryptFile()
        elif opt.text() == "Decrypt File":
            self.OpenDecryptFile()
        elif opt.text() == "Sign File":
            self.OpenSignFile()
        elif opt.text() == "Verify Sign":
            self.OpenVerifySign()
        elif opt.text() == "Generate asymmetric keys":
            self.OpenGenerateKeyWindow()
        else:
            self.OpenEditProfile()
    
    def ClearAllWindow(self):
        for i in range(1, self.vblayout.count()):
            widget_rm = self.vblayout.takeAt(i).widget()
            self.vblayout.removeWidget(widget_rm)
            widget_rm.setParent(None)
    
    def OpenEncryptFile(self):
        self.ClearAllWindow()
        self.vblayout.addWidget(self.encr)

    def OpenDecryptFile(self):
        self.ClearAllWindow()
        self.vblayout.addWidget(self.decr)

    def OpenSignFile(self):
        self.ClearAllWindow()
        self.vblayout.addWidget(self.sign)

    def OpenVerifySign(self):
        self.ClearAllWindow()
        self.vblayout.addWidget(self.verify)

    def OpenGenerateKeyWindow(self):
        self.ClearAllWindow()
        self.vblayout.addWidget(self.gen_keys)
    
    def OpenEditProfile(self):
        self.ClearAllWindow()
        self.vblayout.addWidget(self.edit_profile)


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

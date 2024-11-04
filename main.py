from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from Form import Ui_MainWindow
from Connection import Ui_Connection
import sys
import subprocess


class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.setText("")
        self.ui.pushButton.clicked.connect(self.Update) 
        self.Update()


    def Update(self):
        self.data = self.GetInfo()
        self.ui.label.setText(self.data[0])

        self.widget  = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        for i in range(1, len(self.data)):
            button = QtWidgets.QPushButton(self.data[i], self)
            button.setGeometry(100, 100, 1120, 31)
            button.setStyleSheet("font: 11pt \"Sans Serif\"; color: rgb(0, 0, 0); text-align:left")

            stop = 0
            for j in range(27, 100):
                if self.data[0][j] == "M":
                    stop = j - 1
                    break

            button.clicked.connect(lambda state, x=self.data[i][27:stop].strip():self.Connect(x))
            self.vbox.addWidget(button)

        self.vbox.addStretch()
        self.widget.setLayout(self.vbox)
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.setWidget(self.widget)

    def Connect(self, name):
        self.ConnectionForm = Connection(name)
        self.ConnectionForm.show()

    def GetInfo(self):
        return subprocess.run(["nmcli", "device", "wifi", "list"], text=True, capture_output=True).stdout.rstrip().split("\n")
    

class Connection(QtWidgets.QMainWindow):
    def __init__(self, name):
        super(Connection, self).__init__()
        self.ui = Ui_Connection()
        self.ui.setupUi(self)
        self.ui.label.setStyleSheet("font: 12pt \"Sans Serif\";")
        self.ui.label.setText(name)
        self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit.setFocus()
        self.ui.pushButton.clicked.connect(lambda: self.close())
        self.ui.pushButton_2.clicked.connect(self.ConnectToWiFi)
        self.ui.pushButton_3.clicked.connect(self.toggleVisability)
        
    def toggleVisability(self):
        if self.ui.lineEdit.echoMode() == QtWidgets.QLineEdit.Normal:
            self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)

    def ConnectToWiFi(self):
        result = subprocess.run(["nmcli", "device", "wifi", "connect", self.ui.label.text(), "password", self.ui.lineEdit.text()], text=True, capture_output=True).stdout
        err = subprocess.run(["nmcli", "device", "wifi", "connect", self.ui.label.text(), "password", self.ui.lineEdit.text()], text=True, capture_output=True).stderr
        if "successfully" in result:
            self.close()
            application.update()
        elif "security" in err:
            self.ui.label_3.setText("Wrong Password")
        else:
            self.ui.label_3.setText("Other error")

    def keyPressEvent(self, e):
        if e.key() + 1 == Qt.Key.Key_Enter:
            self.ConnectToWiFi()


app = QtWidgets.QApplication([])
application = window()
application.show()

sys.exit(app.exec())

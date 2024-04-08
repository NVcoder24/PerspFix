from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QRect
import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QFormLayout,
    QFileDialog,
    QPushButton,
    QSlider,
    QCheckBox,
    QMessageBox,
    QSpinBox,
    QFrame,
    QLineEdit,
    QComboBox,
    QLayout
)
import json
import subprocess

img_path = None
presets = []

class Info(QMessageBox):
    def __init__(self, title:str, text:str, info:str):
        super().__init__()

        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)

        self.setText(text)
        self.setInformativeText(info)

        self.show()

        self.exec_()

class Error(QMessageBox):
    def __init__(self, title:str, text:str, info:str):
        super().__init__()

        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(title)

        self.setText(text)
        self.setInformativeText(info)

        self.show()

        self.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(271, 247)
        self.setMaximumSize(271, 247)
        self.setMinimumSize(271, 247)
        self.setWindowTitle("PerspFix trapezoid GUI")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(40, 30, 181, 161))
        self.label.setText("")
        self.label.setPixmap(QPixmap("Screenshot_502.png"))

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QRect(150, 40, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100000)

        self.spinBox_2 = QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QRect(130, 100, 42, 22))
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(100000)

        self.spinBox_3 = QSpinBox(self.centralwidget)
        self.spinBox_3.setGeometry(QRect(150, 170, 42, 22))
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(100000)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(10, 0, 251, 31))
        self.label_2.setText(f"Image path: {img_path}")

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(120, 220, 141, 21))
        self.pushButton.setText("Launch")

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QRect(10, 220, 101, 21))
        self.comboBox.addItems([""] + [ i["name"] for i in presets ])

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QRect(10, 200, 101, 21))
        self.label_3.setText(f"Set preset:")

        self.spinBox.valueChanged.connect(self.sb1_changed)
        self.spinBox_2.valueChanged.connect(self.sb2_changed)
        self.spinBox_3.valueChanged.connect(self.sb3_changed)
        self.comboBox.currentIndexChanged.connect(self.cb_changed)
        self.pushButton.pressed.connect(self.btn_pressed)

        self.setCentralWidget(self.centralwidget)

    def sb1_changed(self):
        self.comboBox.setCurrentIndex(0)

    def sb2_changed(self):
        self.comboBox.setCurrentIndex(0)

    def sb3_changed(self):
        self.comboBox.setCurrentIndex(0)

    def btn_pressed(self):
        try:
            DETACHED_PROCESS = 0x00000008
            results = subprocess.Popen(['main.exe', str(img_path), str(1), str(self.spinBox.value()), str(self.spinBox_2.value()), str(self.spinBox_3.value())],
                    close_fds=True, creationflags=DETACHED_PROCESS)
            sys.exit()
        except Exception as e:
            Error("Error", f"Failed to launch main.exe:\n{e}", "")

    def cb_changed(self):
        i = self.comboBox.currentIndex()
        if i > 0:
            self.spinBox.setValue(presets[i - 1]["wt"])
            self.spinBox_2.setValue(presets[i - 1]["h"])
            self.spinBox_3.setValue(presets[i - 1]["wb"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("trapezoid.json", encoding="utf-8") as f:
            presets = json.loads(f.read())
    except Exception as e:
        Error("No presets!", "Read/parsing trapezoid.json failed", "")
        sys.exit()
    try:
        img_path = sys.argv[1]
    except Exception as e:
        Error("Error", "Incorrect image path!", "")
        sys.exit()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

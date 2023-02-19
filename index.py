import os
import subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

def on_mon_bouton_clicked():
        subprocess.run(['python', 'mission_debutant.py'])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = uic.loadUi("./index.ui")
    window.show()
    window.openfile.clicked.connect(on_mon_bouton_clicked)
    app.exec_()

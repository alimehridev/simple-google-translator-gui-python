from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, qApp
from PyQt5 import QtCore
import sys
import time
import threading
 
class Notification:
   def __init__(self, text = ""):
      super().__init__()
      self.app = QApplication(sys.argv)
      self.win = QWidget()
      self.grid = QGridLayout()
      self.win.setLayout(self.grid)
      self.win.setWindowOpacity(0.999)

      screen = self.app.primaryScreen().size()
      self.screenWidth = screen.width()
      self.screenHeight = screen.height()
      self.width = 250
      self.height = 100
      self.win.setGeometry(self.screenWidth - self.width - 10, self.screenHeight - self.height, self.width, self.height)
      self.win.setWindowTitle("PyQt5 window")
      self.win.setWindowFlag(QtCore.Qt.FramelessWindowHint)

      self.closeBtn = QLabel("X", self.win)
      self.closeBtn.setStyleSheet("padding: 10 10 10 10")

      self.textLabel = QLabel(text, self.win)
      self.grid.addWidget(self.textLabel, 1, 0)
      self.win.show()
      QtCore.QTimer.singleShot(5000, self.app.exit)
      sys.exit(self.app.exec_())



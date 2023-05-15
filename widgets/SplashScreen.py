from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSplashScreen

from project_resources import SplashScreenBackground


class SplashScreen(QSplashScreen):
    def __init__(self, parent=None):
        QSplashScreen.__init__(self, parent=parent)
        self.mainFormHandle = self.parent()
        self.W = 600
        self.H = 400
        self.setFixedSize(self.W, self.H)
        self.setPixmap(QPixmap(SplashScreenBackground))

        self.show()

    def advProgressFcn(self, aStr):
        self.showMessage(aStr, alignment=Qt.AlignBottom | Qt.AlignHCenter,
                         color=Qt.black)

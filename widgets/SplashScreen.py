import sys

from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QSplashScreen, QApplication


class SplashScreen(QSplashScreen):
    def __init__(self, parent=None):
        QSplashScreen.__init__(self)
        self.mainFormHandle = self.parent()
        self.W = 600
        self.H = 400
        self.setFixedSize(self.W, self.H)
        bkgPath = "res/icons/TCSsplachScreen.png"
        localPath = QDir().filePath(bkgPath)
        pixmap = QPixmap(localPath)
        self.setPixmap(pixmap)

        # desktop = QApplication.desktop()
        # screenWidth = desktop.width()
        # screenHeight = desktop.height()
        # x = int((screenWidth - self.W) / 2)
        # y = int((screenHeight - self.H) / 2)
        # self.resize(self.W, self.H)
        # self.move(x, y)

        self.splashFont = QFont("Segoe UI", 10, QFont.Normal)
        self.setFont(self.splashFont)

        self.show()

    def advProgressFcn(self, aStr):
        self.showMessage(aStr, alignment=Qt.AlignBottom | Qt.AlignHCenter,
                         color=Qt.black)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ss = SplashScreen()
    ss.show()
    sys.exit(app.exec_())

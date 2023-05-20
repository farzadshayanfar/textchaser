import sys

from PySide6.QtWidgets import QApplication

from widgets import MainForm
import themes

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(themes.zagros_light_qss)
    textChaser = MainForm()
    textChaser.show()
    sys.exit(app.exec())

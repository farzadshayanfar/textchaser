import sys

from PySide6.QtWidgets import QApplication

from widgets import MainForm, themes

if __name__ == "__main__":
    app = QApplication(sys.argv)
    textChaser = MainForm()
    app.setStyleSheet(themes.zagros)
    textChaser.show()
    sys.exit(app.exec())

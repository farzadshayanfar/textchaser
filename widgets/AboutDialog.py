from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class AboutDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowTitle("About")
        self.setWindowIcon(QIcon("res/icons/TextChaser2.png"))
        self.aLabel = QLabel()
        self.aBtn = QPushButton("Okay")
        self.aBtn.clicked.connect(lambda: self.close())
        self.aLabel.setText("""
        <h3 style="text-align: center;"><em><strong><img src="res/icons/TextChaser2.png" alt="" width="105" height="105" /></strong></em></h3>
<h3 style="text-align: center;"><em><strong>Welcome to TextChaser!</strong></em></h3>
<p style="text-align: center;">TextChaser uses Google Tesseract engine for text extraction from scene 
or document image files. We have optimized the software for working with Farsi, English and Farsi-English documents.</p>
<p style="text-align: center;">Developed by Farzad Shayanfar.
</p>
<p style="text-align: center;">Summer 2019.</p>
        """)
        self.aLabel.setWordWrap(True)
        self.setFixedSize(300, 400)
        self.theLayout = QVBoxLayout()
        self.setLayout(self.theLayout)
        # self.layout().addWidget(self.iconPixMapLbl)
        self.theLayout.addWidget(self.aLabel)

        self.theLayout.addWidget(self.aBtn, 1, Qt.AlignHCenter)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

import project_resources


class AboutDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowTitle("About")
        self.setWindowIcon(QPixmap(project_resources.AppIconPath))
        self.contentLabel = QLabel()
        self.okayButton = QPushButton("Okay")
        self.okayButton.clicked.connect(lambda: self.close())
        self.contentLabel.setText(f"""
        <div style="text-align: center;">
        <img src={project_resources.AppIconPath} alt="" width="110" height="110" />
        </div>
        <h3 style="text-align: center;"><em><strong>Welcome to TextChaser!</strong></em></h3>
        <p style="padding: 10px">
        TextChaser uses Google Tesseract engine for text extraction from scene or document image files. 
        We have optimized the software for working with Farsi, English and Farsi-English documents.
        </p>
        <p style="text-align: center;">Developed by Farzad Shayanfar.
        </p>
        <p style="text-align: center;">Summer 2019.</p>
        """)
        self.contentLabel.setWordWrap(True)
        self.setFixedSize(300, 400)
        self.theLayout = QVBoxLayout()
        self.setLayout(self.theLayout)
        self.theLayout.addWidget(self.contentLabel)

        self.theLayout.addWidget(self.okayButton, 1, Qt.AlignHCenter)

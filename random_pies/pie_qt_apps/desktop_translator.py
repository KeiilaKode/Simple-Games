from PyQt6.QtCore import Qt
from PyQt6.QtGui import QInputEvent
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, \
    QTextEdit, QComboBox
from PyQt6.QtGui import QFont
from textual.css.types import AlignHorizontal, AlignVertical

from random_pies.emporium_map_app import master_layout


class Translator(QWidget):
    def __init__(self):
        super().__init__()

        self.setup()


    def setup(self):
        self.setGeometry(375, 75, 900, 725)
        self.setWindowTitle("Translator 2026")
        self.initUI()

    def initUI(self):
        self.text_box1 = QTextEdit()
        self.text_box1.setFont(QFont("Helvetica", 32))
        self.text_box1.setStyleSheet("QLineEdit {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 10px; background: #444444; color: #54b5fd;}")
        self.text_box1.setReadOnly(False)

        self.text_box2 = QTextEdit()
        self.text_box2.setFont(QFont("Helvetica", 32))
        self.text_box2.setStyleSheet("QLineEdit {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 10px; background: #444444; color: #54b5fd;}")
        self.text_box2.setReadOnly(True)

        # Create columns
        self.col1 = QVBoxLayout()   # skinny tall rectangle on the left side
        self.logo_words = QLabel("PyLate")
        self.col1.addWidget(self.logo_words)
        self.col1.addWidget(QComboBox())
        self.col1.addWidget(QComboBox())
        self.col1.addWidget(QPushButton())
        self.col1.addWidget(QPushButton("Clear"))


        self.col2 = QVBoxLayout()     # tall rectangle on the right side
        self.col2.addWidget(self.text_box1)
        self.col2.addWidget(QPushButton("Reverse"))
        self.col2.addWidget(self.text_box2)



        # Design app
        master_layout = QHBoxLayout()
        master_layout.addLayout(self.col1, 1)
        master_layout.addLayout(self.col2, 3)
        self.setLayout(master_layout)

if __name__ == "__main__":
    app = QApplication([])
    window = Translator()
    window.show()
    app.exec()



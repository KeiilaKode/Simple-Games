from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QComboBox
from PyQt6.QtGui import QFont
import asyncio
from googletrans import Translator
from languages import *


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()


    def setup(self):
        self.setGeometry(375, 75, 900, 725)
        self.setWindowTitle("Translator 2026")
        self.initUI()
        self.events()


    # Design and Layout
    def initUI(self):

        # Left side
        self.title = QLabel("""   PyLateR
TransMitteR""")
        self.title.setFont(QFont("Lucida Handwriting", 30)) # Lucida Handwriting
        self.title.setStyleSheet("QLabel {padding: 2px; color: #54b5fd;}")
        self.input_option = QComboBox()
        self.input_option.setFont(QFont("Helvetica", 10))
        self.input_option.setStyleSheet("QComboBox {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 6px; background: #444444; color: #54b5fd;}")

        self.output_option = QComboBox()
        self.output_option.setFont(QFont("Helvetica", 10))
        self.output_option.setStyleSheet("QComboBox {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 6px; background: #444444; color: #54b5fd;}")

        self.trans_button = QPushButton("Translate")
        self.trans_button.setFont(QFont("Helvetica", 20))
        self.trans_button.setStyleSheet("QPushButton {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 10px; background: #444444; color: #54b5fd;}")

        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(QFont("Helvetica", 20))
        self.clear_button.setStyleSheet("QPushButton {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 10px; background: #444444; color: #54b5fd;}")

        # Right side
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Enter Passage here...")
        self.input_box.setFont(QFont("Helvetica", 20))
        self.input_box.setStyleSheet("QTextEdit {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 10px; background: #444444; color: #54b5fd;}")
        self.input_box.setReadOnly(False)
        self.reverse_button = QPushButton("Reverse")
        self.reverse_button.setFont(QFont("Helvetica", 20))
        self.reverse_button.setStyleSheet("QPushButton {border:3px solid #ff99ff; border-radius: 10px;"
                                     "padding: 10px; background: #444444; color: #54b5fd;}")

        self.output_box = QTextEdit()
        self.output_box.setFont(QFont("Helvetica", 20))
        self.output_box.setStyleSheet("QTextEdit {border:3px solid #ff99ff; border-radius: 10px;"
                                      "padding: 10px; background: #444444; color: #54b5fd;}")
        #self.output_box.setReadOnly(True)
        self.input_option.addItems(values)
        self.output_option.addItems(values)
        self.input_option.setCurrentIndex(21)

        # Layouts
        master_layout = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        widgets1 = [self.title, self.input_option, self.output_option, self.trans_button, self.clear_button] # ,
        for widget in widgets1:
            col1.addWidget(widget)

        widgets2 = [self.input_box, self.reverse_button, self.output_box]
        for widget in widgets2:
            col2.addWidget(widget)

        master_layout.addLayout(col1, 1)
        master_layout.addLayout(col2, 3)
        self.setLayout(master_layout)


    def events(self):
        self.trans_button.clicked.connect(self.translate_click)
        self.clear_button.clicked.connect(self.clear_text)
        self.reverse_button.clicked.connect(self.reverse_text)


    async def translate_text(self, text, dest_lang, src_lang):
        translator = Translator()
        translation = await translator.translate(text, dest=dest_lang, src=src_lang)
        return translation.text


    def translate_click(self):
        try:
            value_to_key1 = self.input_option.currentText() # English
            key_to_value1 = [key for key, value in LANGUAGES.items() if value == value_to_key1] # [en]
            value_to_key2 = self.output_option.currentText()  # English
            key_to_value2 = [key for key, value in LANGUAGES.items() if value == value_to_key2]
            self.script = asyncio.run(self.translate_text(self.input_box.toPlainText(), key_to_value2[0], key_to_value1[0]))
            self.output_box.setText(self.script)
        except Exception as e:
            print(f"ERROR: {e}")
            self.output_box.setText("You must enter text to translate.")


    def clear_text(self):
        self.input_box.clear()
        self.output_box.clear()


    def reverse_text(self):
        input1, input2 = self.input_option.currentText(), self.input_box.toPlainText()
        output1, output2 = self.output_option.currentText(), self.output_box.toPlainText()
        self.input_option.setCurrentText(output1)
        self.output_option.setCurrentText(input1)
        self.input_box.setText(output2)
        self.output_box.setText(input2)


if __name__ == "__main__":
    app = QApplication([])
    window = TranslatorApp()
    window.show()
    app.exec()




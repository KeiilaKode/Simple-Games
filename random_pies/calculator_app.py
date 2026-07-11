from PyQt6.QtCore import Qt
from PyQt6.QtGui import QInputEvent
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QFont

# Class takes QWidget as super class
class CalcApp(QWidget):
    def __init__(self):
        super().__init__()
        self.app_settings()
        self.initUI()
        self.button_events()

    def app_settings(self):
        self.setGeometry(480, 150, 300, 500)
        self.setWindowTitle("My Calculator")
        # background color
        self.setObjectName("CalculatorBackground")
        self.setStyleSheet("#CalculatorBackground { background-color: #B0B0B0; }") # #30054d #1e1e2e

    def initUI(self):
        # Create app objects
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("Helvetica", 32))  # QFont also uses .setStyleSheet() Decorative
        self.text_box.setStyleSheet("QLineEdit {border:3px solid #ff99ff; border-radius: 10px;"
                                    "padding: 10px; background: #444444; color: #54b5fd;}") #333 black
        self.text_box.setReadOnly(True)

        # Creates the grid
        self.grid = QGridLayout()
        self.buttons = ["7", "8", "9", "/",
                   "4", "5", "6", "*",
                   "1", "2", "3", "-",
                   "0", ".", "=", "+"]
        # Buttons
        self.button_clear = QPushButton("Clear")
        self.button_delete = QPushButton("Delete")

        self.button_clear.setStyleSheet(self.get_button_style())
        self.button_delete.setStyleSheet(self.get_button_style())
        # Add the buttons to the Grid, starting at 0, inserts the grid above the row layout made above
        row = 0
        col = 0
        # Create button for each element in button list
        for text in self.buttons:
            # Creates a button every loop, applies text from list to it
            button = QPushButton(text)
            button.clicked.connect(self.button_click)
            # Styles the rest of the button's font *************
            button.setStyleSheet(self.get_button_style())
            # Create an event here
            self.grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Design the App, main column container
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)
        master_layout.setContentsMargins(20, 20, 20, 20)  # Sets the padding around all widgets and outer edge
        row = QHBoxLayout()
        row.addWidget(self.button_clear)  # , alignment=Qt.AlignmentFlag.AlignLeft
        row.addWidget(self.button_delete)  # , alignment=Qt.AlignmentFlag.AlignRight
        master_layout.addLayout(row)
        # Combines all layouts to make the full app window layout
        self.setLayout(master_layout)


    # this is pink in hexadecimal #fd00d6: and #ff99ff
    # dark grey #444444: light grey #777777 teal #ff99ff #ff99ff #444444 #333
    def get_button_style(self):
        return """
    QPushButton {
        font: 23pt Helvetica;
        border: 3px solid #ff99ff;
        border-radius: 15px;
        background-color: #444444;
        color: #54b5fd;
        padding: 15px;
        
    }
    QPushButton:hover{
    background-color: #eee
    }
    QPushButton:pressed {
    background-color: #330160
    }
    
    """

    def button_events(self):
        self.button_clear.clicked.connect(self.button_click)
        self.button_delete.clicked.connect(self.button_click)

    # Add functionality
    def button_click(self):
        button = app.sender()
        text = button.text()  # gets the text string from button
        if text == "=":
            # 2 + 2
            symbol = self.text_box.text()
            try:
                res = eval(symbol)
                self.text_box.setText(str(res))
            except Exception as e:
                print("Error", e)

        elif text == "Clear":
            self.text_box.clear()

        elif text == "Delete":
            current_value = self.text_box.text()  # 3 + 9....remove the 9
            self.text_box.setText(current_value[:-1])

        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)


if __name__ == "__main__":
    app = QApplication([])
    window = CalcApp()
    window.show()
    app.exec()


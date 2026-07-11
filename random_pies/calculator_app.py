from PyQt6.QtCore import Qt
from PyQt6.QtGui import QInputEvent
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QFont




# Settings
app = QApplication([])
window = QWidget()
window.setGeometry(480, 150, 300, 500)
window.setWindowTitle("My Calculator")

# Create app objects
text_box = QLineEdit()
text_box.setFont(QFont("Helvetica", 32)) #QFont also uses .setStyleSheet() Decorative

# Creates the grid
grid = QGridLayout()
buttons = ["7", "8", "9", "/",
               "4", "5", "6", "*",
               "1", "2", "3", "-",
               "0", ".", "=", "+"]
# Buttons
button_clear = QPushButton("Clear")
button_delete = QPushButton("Delete")

# Style buttons
button_clear.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding:10px; }")
button_delete.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding:10px; }")

# Design the App, main column container
master_layout = QVBoxLayout()
master_layout.addWidget(text_box)
master_layout.addLayout(grid)
# Sets the padding around all widgets and outer edge
master_layout.setContentsMargins(20, 20, 20, 20)

row = QHBoxLayout()
row.addWidget(button_clear) # , alignment=Qt.AlignmentFlag.AlignLeft
row.addWidget(button_delete) # , alignment=Qt.AlignmentFlag.AlignRight

# row is added to master_layout last so it puts it at the bottom
master_layout.addLayout(row)

# Combines all layouts to make the full app window layout
window.setLayout(master_layout)

# Add the buttons to the Grid, starting at 0, inserts the grid above the row layout made above
row = 0
col = 0

# Methods in PyQt to use for logic: .text(), .clear(), eval(), .sender()

# Add functionality
def button_click():
    button = app.sender()
    text = button.text() # gets the text string from button

    if text == "=":
        # 2 + 2
        symbol = text_box.text()
        try:
            res = eval(symbol)
            text_box.setText(str(res))
        except Exception as e:
            print("Error", e)

    elif text == "Clear":
        text_box.clear()

    elif text == "Delete":
        current_value = text_box.text() # 3 + 9....remove the 9
        text_box.setText(current_value[:-1])

    else:
        current_value = text_box.text()
        text_box.setText(current_value + text)

# Create button for each element in button list
for text in buttons:
    # Creates a button every loop, applies text from list to it
    button = QPushButton(text)
    button.clicked.connect(button_click)
    # Styles the rest of the button's font
    button.setStyleSheet("QPushButton {font: 25pt Comic Sans MS; padding:10px; }")
    # Create an event here
    grid.addWidget(button, row, col)
    col += 1
    if col > 3:
        col = 0
        row +=1

button_clear.clicked.connect(button_click)
button_delete.clicked.connect(button_click)

# Styles the rest of the button's font





if __name__ == "__main__":
    window.show()
    app.exec()


# Take grid layout, add button, to this row and this column, needs 18 buttons
#grid.addWidget(button, row, col)

# Make row/column index of 5: # first row/cols, index start at 0
# To add the number 5 to button, it would be (row2,col1)

# row = 0
# col = 0
# def make_grid():
#     for button_text in buttons:
#         button = QPushButton(button_text)
#         button.clicked.connect(button_click)
#         grid.addWidget(button, row, col)
#         col += 1
#         if col > 3:
#             col = 0
#             row += 1
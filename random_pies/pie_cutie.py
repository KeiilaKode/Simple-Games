from PyQt6.QtCore import Qt # For alignment
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from random import choice
#QVBoxLayout() # Vertical, Columns # QHBoxLayout() # Horizontal, Rows

# Create App and Window
app = QApplication([])      # create app and window
window = QWidget()       # window is an object, = is the class
window.setGeometry(625, 250, 500, 300)     #  x, y, w, h
window.setWindowTitle("Aaron's App")    # object. method from QWidget class, names the whole window

# Create all the Widgets, the objects we see on the screen
title_text = QLabel("Random Word Generator")
text1 = QLabel("?")
text2 = QLabel("?")
text3 = QLabel("?")

# Widgets, but still need to be put in a container
button1 = QPushButton("Click Me")
button2 = QPushButton("Don'tClick Me")
button3 = QPushButton("Or Click Me")

# Create the design/ assigned containers
master_layout = QVBoxLayout()    # Main Column
row1 = QHBoxLayout()             # Rows inside Column
row2 = QHBoxLayout()             # Rows inside Column
row3 = QHBoxLayout()             # Rows inside Column/ master_layout

# Layouts
row1.addWidget(title_text, alignment=Qt.AlignmentFlag.AlignCenter)
row2.addWidget(text1, alignment=Qt.AlignmentFlag.AlignLeft)
row2.addWidget(text3, alignment=Qt.AlignmentFlag.AlignCenter)
row2.addWidget(text2, alignment=Qt.AlignmentFlag.AlignRight)

row3.addWidget(button1, alignment=Qt.AlignmentFlag.AlignLeft)
row3.addWidget(button2, alignment=Qt.AlignmentFlag.AlignCenter)
row3.addWidget(button3, alignment=Qt.AlignmentFlag.AlignRight)

master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)
window.setLayout(master_layout)


# Creating the functionality
my_words = ["Lovely", "Gangster", "Hello", "Loser", "Test", "Python", "I'm the best", "Winner"]
def test_button():
    print("This button is working!")

def random_word1():
    word = choice(my_words)
    text1.setText(word)

def random_word2():
    word = choice(my_words)
    text2.setText(word)

def random_word3():
    word = choice(my_words)
    text3.setText(word)

# Event: Clicked , Connects buttons being clicked to calling the functions
button1.clicked.connect(random_word1)
button2.clicked.connect(random_word3)
button3.clicked.connect(random_word2)





# Event of being clicked, connects to function

# Changes word output













if __name__ == "__main__":
    window.show()
    # Runs app
    app.exec()




from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.link = "Not set"

        self.setWindowTitle("Mars Map")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.set_text)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def set_text(self, data):
        self.link = data
        self.label.setText(f"Current link: {data}")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
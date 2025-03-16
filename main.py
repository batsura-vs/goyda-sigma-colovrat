import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

app = QApplication(sys.argv)

PAGE = QStackedWidget()


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

        button = QPushButton(text="Далее")
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def set_text(self, data):
        self.link = data
        self.label.setText(f"Current link: {data}")


class MapWindow(QMainWindow):
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

        button = QPushButton(text="Далее")
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def set_text(self, data):
        self.link = data
        self.label.setText(f"Current link: {data}")

PAGE.addWidget(MainWindow())
PAGE.show()

app.exec()

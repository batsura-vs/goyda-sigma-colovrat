import json
from os import read
import sys
from windows import show_plot as nigga
import numpy as np
import requests
from matplotlib import pyplot as plt
from matplotlib.ticker import LinearLocator
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

app = QApplication(sys.argv)
map_window = None
url = None
PAGE = QStackedWidget()


def load_and_save():
    unique = []
    z = 0
    while z != 16:
        a = requests.get(f"{url}/ppo_it/api").json()
        status = a["status"]

        if status == "ok":
            tile = a["message"]["data"]

            if tile not in unique:
                unique.append(tile)
                z += 1
                yield z
    with open("ЛУЧШАЯ СУБД.json", "w") as f:
        json.dump(unique, f)


def show_plot(sender=None, listener=None):
    with open("ЛУЧШАЯ СУБД.json", "r") as f:
        unique = json.load(f)
    error = True
    while error:
        try:
            nigga(unique=unique, sender=sender, listener=listener)
            error = False
        except Exception as e:
            load_and_save()
            print(e)
            error = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.link = "Not set"

        self.setWindowTitle("Mars Map")

        self.label = QLabel()
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(25, 45, 335, 30)
        self.progressBar.move(200, 100)

        self.input = QLineEdit()
        self.input.textChanged.connect(self.set_text)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        self.button = QPushButton(text="Далее")
        self.button.clicked.connect(self.ready)
        layout.addWidget(self.button)
        layout.addWidget(self.progressBar)
        self.last = QPushButton(text="Открыть последнее")
        self.last.clicked.connect(self.open_last)
        layout.addWidget(self.last)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def set_text(self, data):
        self.link = data
        self.label.setText(f"Current link: {data}")

    def open_last(self):
        show_plot()

        # show_plot(sender=(20, 20), listener=(60, 60))
        self.close()
        PAGE.setCurrentWidget(map_window)

    def ready(self):
        self.setDisabled(True)
        global url
        url = self.link
        with open("url", "w") as f:
            f.write(url)
        try:
            for p in load_and_save():
                self.progressBar.setValue(int(100 / 16 * p))
        except:
            pass
        show_plot()

        # show_plot(sender=(20, 20), listener=(60, 60))
        self.close()
        PAGE.setCurrentWidget(map_window)


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.link = "Not set"

        self.setWindowTitle("Mars Map")

        self.label = QLabel()

        layout = QVBoxLayout()

        button = QPushButton(text="Отображение расположения базовых станций")
        button.clicked.connect(self.ready)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def ready(self):
        with open("url", "r") as f:
            url = f.read()
        data = requests.get(f"{url}/ppo_it/api/coords").json()["message"]
        plt.close()
        show_plot(sender=data["sender"], listener=data["listener"])


PAGE.show()
map_window = MapWindow()
PAGE.addWidget(MainWindow())
PAGE.addWidget(map_window)

app.exec()

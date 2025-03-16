import json
from os import read
import sys

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
PAGE = QStackedWidget()

def load_and_save(url):
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

def show_plot():
    with open("ЛУЧШАЯ СУБД.json", "r") as f:
        unique = json.load(f)
    pdiddy = np.array(unique)
    data = []
    for i in range(0, 16, 4):
        data.append(np.hstack((pdiddy[i], pdiddy[i + 1], pdiddy[i + 2], pdiddy[i + 3])))

    data = np.array(data).reshape(256, 256)
    print(data.shape)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    X = np.array([i for i in range(256)])
    Y = np.array([i for i in range(256)])
    X, Y = np.meshgrid(X, Y)
    Z = np.array(data)
    surf = ax.plot_surface(
        X,
        Y,
        Z,
        # cmap=cm.coolwarm, #COLOR
        color="b",
        linewidth=0,
        antialiased=False,
    )
    ax.set_zlim(0, 1000)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter("{x:.02f}")

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


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

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def set_text(self, data):
        self.link = data
        self.label.setText(f"Current link: {data}")

    def ready(self):
        self.setDisabled(True)
        for p in load_and_save(self.link):
            self.progressBar.setValue(int(100 / 16 * p))
        show_plot()
        self.close()
        PAGE.setCurrentWidget(map_window)
        


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
        button.clicked.connect(self.ready)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def set_text(self, data):
        self.link = data
        self.label.setText(f"Current link: {data}")
        plt.close()

    def ready(self):
        plt.close()
        show_plot()

PAGE.show()
map_window = MapWindow()
PAGE.addWidget(MainWindow())
PAGE.addWidget(map_window)

app.exec()

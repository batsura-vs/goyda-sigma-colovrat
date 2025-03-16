import matplotlib.pyplot as plt
import numpy as np
import requests
from matplotlib.ticker import LinearLocator

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
data = requests.get("https://olimp.miet.ru/ppo_it/api")
data = data.json()["message"]["data"]


def show_surface(data):
    X = np.array([i for i in range(64)])
    Y = np.array([i for i in range(64)])
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

    ax.set_zlim(0, 255)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter("{x:.02f}")

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


show_surface(data)

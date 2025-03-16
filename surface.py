import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LinearLocator
import requests

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# unique = [
#     [[[1] * 64] * 64]
# ] * 16
unique = []
z = 0
while z != 16:
    a = requests.get('https://olimp.miet.ru/ppo_it/api').json()
    status = a["status"]

    if status == "ok":
        tile = a["message"]["data"]

        if tile not in unique:
            unique.append(tile)
            z += 1

# with open("uni.json", "w") as f:
#     json.dump(unique, f)
# with open("uni.json", "r") as f:
#     unique = json.load(f)

# print(unique)
# unique = sorted(unique, key=lambda x: sum([i.count(255) for i in x]))
# print(np.array(unique).shape)
# unique = requests.get('https://olimp.miet.ru/ppo_it/api').json()["message"]["data"]
# unique = np.array(unique).reshape(64, 64)
# unique = [
#     [(x + y) // 4 for x in range(256)]
#     for y in range(256)
# ]
# data = [
#     [0 for _ in range(256)]
#     for _ in range(256)
# ]
# for cur_tile, tile in enumerate(unique):
#     for tile_z, z in enumerate(tile):
#         # if (cur_tile + 1) % 64 == 0:
#         pass
print(np.array(unique).shape)
pdiddy = np.array(unique)
data = []
for i in range(0, 16, 4):
    data.append(np.hstack((pdiddy[i], pdiddy[i + 1], pdiddy[i + 2], pdiddy[i + 3])))

data = np.array(data).reshape(256, 256)
print(data.shape)

def show_surface(data, x, y):
    X = np.array([i for i in range(x)])
    Y = np.array([i for i in range(y)])
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


show_surface(data, 256, 256)

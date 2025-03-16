from csv import reader
import matplotlib.pyplot as plt
import numpy as np
import requests
from matplotlib.ticker import LinearLocator


def show_plot(unique, sender=None, listener=None):
    def suma_up(tile):
        return sum(tile[0])

    def suma_down(tile):
        return sum(tile[-1])

    def suma_right(tile):
        s = 0
        for i in range(len(tile)):
            s += tile[i][-1]
        return s

    def suma_left(tile):
        s = 0
        for i in range(len(tile)):
            s += tile[i][0]
        return s


    #print(unique)

    delta = 500

    tile_1, tile_2, tile_3, tile_4, tile_5, tile_6, tile_7, tile_8, tile_9, tile_10, tile_11, tile_12, tile_13, tile_14, tile_15, tile_16  = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]


    lefts = []
    ups = []
    downs = []
    rights = []

    center = []
    for i in unique:

        flag = False

        if suma_down(i) == 64*255:
            flag = True
            downs.append(i)

        if suma_up(i) == 64*255:
            flag = True
            ups.append(i)

        if suma_left(i) == 64*255:
            flag = True
            lefts.append(i)

        if suma_right(i) == 64*255:
            flag = True
            rights.append(i)

        if flag == False:
            center.append(i)


    for i in lefts:
        if suma_up(i) == 64*255:
            tile_1 = i

        if suma_down(i) == 64*255:
            tile_13 = i

    lefts.pop(lefts.index(tile_1))
    lefts.pop(lefts.index(tile_13))

    if abs(suma_down(lefts[0]) - suma_up(lefts[1])) <= delta:
        tile_5 = lefts[0]
        tile_9 = lefts[1]
    else:
        tile_5 = lefts[1]
        tile_9 = lefts[0]

    #=========
    for i in rights:
        if suma_up(i) == 64*255:
            tile_4 = i

        if suma_down(i) == 64*255:
            tile_16 = i

    rights.pop(rights.index(tile_4))
    rights.pop(rights.index(tile_16))

    if abs(suma_down(rights[0]) - suma_up(rights[1])) <= delta:
        tile_8 = rights[0]
        tile_12 = rights[1]
    else:
        tile_12 = rights[1]
        tile_8 = rights[0]

    #=========
    ups.pop(ups.index(tile_1))
    ups.pop(ups.index(tile_4))

    if abs(suma_right(ups[0]) - suma_left(ups[1])) <= delta:
        tile_2 = ups[0]
        tile_3 = ups[1]
    else:
        tile_3 = ups[1]
        tile_2 = ups[0]

    #=========
    downs.pop(downs.index(tile_13))
    downs.pop(downs.index(tile_16))

    if abs(suma_right(downs[0]) - suma_left(downs[1])) <= delta:
        tile_14 = downs[0]
        tile_15 = downs[1]
    else:
        tile_15 = downs[1]
        tile_14 = downs[0]

    #===========

    for i in center:
        if abs(suma_up(i) - suma_down(tile_2)) <= delta and abs(suma_left(i) - suma_right(tile_5)) <= delta:
            tile_6 = i

        if abs(suma_up(i) - suma_down(tile_3)) <= delta and abs(suma_right(i) - suma_left(tile_8)) <= delta:
            tile_7 = i

        if abs(suma_down(i) - suma_up(tile_14)) <= delta and abs(suma_left(i) - suma_right(tile_9)) <= delta:
            tile_10 = i

        if abs(suma_down(i) - suma_up(tile_15)) <= delta and abs(suma_right(i) - suma_left(tile_12)) <= delta:
            tile_11 = i


    unique = [tile_1] + [tile_2] + [tile_3] + [tile_4] + [tile_5] + [tile_6] + [tile_7] + [tile_8] + [tile_9] + [tile_10] + [tile_11] + [tile_12] + [tile_13] + [tile_14] + [tile_15] + [tile_16]
    unique_data = []

    k = 0
    print(len(unique))
    for _ in range(4):
        for i in range(64):
            loc_arr = unique[k][i] + unique[k + 1][i] + unique[k + 2][i] + unique[k + 3][i]
            unique_data.append(loc_arr)
        k += 4

    print(len(unique_data), len(unique_data[0]))

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    data = requests.get("https://olimp.miet.ru/ppo_it/api")
    data = data.json()["message"]["data"]


    def show_surface(data, x_start, x_end, y_start, y_end):
        X = np.array([i for i in range(x_start, x_end + 1)])
        Y = np.array([i for i in range(y_start, y_end + 1)])
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
        if sender:
            ax.scatter(sender[0], sender[1], 1000, color='red', s=50)
        if listener:
            ax.scatter(listener[0], listener[1], 1000, color='red', s=50)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()

    show_surface(unique_data, 0, 255, 0, 255)

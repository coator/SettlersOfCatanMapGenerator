from collections import Counter
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from shapely.geometry import Polygon

pip_values = (2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12)

standard_map_shape = [[-1, 0, 0],
                       [0, 0, 0],
                       [1, 0, 0],
                       [-1.5, -2.5, -1],
                       [-.5, -2.5, -1],
                       [.5, -2.5, -1],
                       [1.5, -2.5, -1],
                       [-2, -3.5, -.5],
                       [-1, -3.5, -.5],
                       [-0, -3.5, -.5],
                       [1, -3.5, -.5],
                       [2, -3.5, -.5],
                       [-1.5, -4.5, 0],
                       [-.5, -4.5, 0],
                       [.5, -4.5, 0],
                       [1.5, -4.5, 0],
                       [-1, -5.5, .5],
                       [0, -5.5, .5],
                       [1, -5.5, .5]
                       ]


class pip:
    def __init__(self, board_location, tile, value):
        self.tile = tile
        self.value = value
        self.board_location = board_location


def rsrc_shfl():
    pr = [
        'field', 'field', 'field', 'field', 'pasture', 'pasture', 'pasture', 'pasture', 'forest', 'forest', 'forest',
        'forest', 'hill', 'hill', 'hill', 'mountain', 'mountain', 'mountain', 'desert']
    # if there are two resources next to each other in the list the numbers will to rerolled
    shuffle(pr)
    item = 0
    while item in range(len(pr) - 1):
        if pr[item] == pr[item + 1]:
            # print(f'Matching resources at {item} and {item + 1}')
            shuffle(pr)
            item = 0
        else:
            item += 1
    return tuple(pr)


def rsrc_divsr_calc(*argv):
    # Resource distribution is calculated by dividing the map into half 3 times, summing the difference of squares
    # on the two sides for each resource.
    total = 0
    for arg in argv:
        differences = Counter(arg[:7] * 6) + Counter(arg[8:12] * 3) - Counter(arg[13:] * 6) + Counter(arg[8:12] * 3)
        # var is squaring the difference amount
        total = + sum(x ** 2 for x in differences.values())
    return total


def rsrc_cluster_calc(catan_map):
    for item in catan_map:
        print(item)
    pass

    # counts 5 points for each corner touching


# [vertical coord,vertical coord,
def catan_map(pr,map_shape):


    map_tiles = []
    for item in range(len(pr)):
        print(map_tiles)
        if pr[item] == 'mountain':
            map_tiles.append(['Red', 'Mountain'])
        elif pr[item] == 'field':
            map_tiles.append(['Yellow', 'Field'])
        elif pr[item] == 'forest':
            map_tiles.append(['#254117', 'Forest '])
        elif pr[item] == 'pasture':
            map_tiles.append(['#52D017', 'Pasture'])
        elif pr[item] == 'hill':
            map_tiles.append(['Brown', 'Hills'])
        elif pr[item] == 'desert':
            map_tiles.append(['White', 'Desert'])
        else:
            print(pr[item])


    # Horizontal cartesian coords
    hcoord = [c[0] for c in map_shape]

    # Vertical cartersian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in map_shape]

    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')

    for x, y, c, l in zip(hcoord, vcoord, map_tiles, map_tiles):
        color = c[0].lower()
        hex = RegularPolygon((x, y), numVertices=6, radius=4. / 7,
                             orientation=np.radians(60),
                             facecolor=color, alpha=0.2, edgecolor='k')
        ax.add_patch(hex)
        # Also add a text label
        ax.text(x, y + 0.2, l[1], ha='center', va='center', size=10)

    # Also add scatter points in hexagon centres
    ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in map_tiles], alpha=0.5)

    plt.show()
    return (plt)


def rsrc_whole_calc(tolerance):
    while True:
        # generates board
        pr = rsrc_shfl()

        # 30 degree shift of tiles to represent 2nd line
        pr2 = (
            pr[7], pr[3], pr[0], pr[12], pr[8], pr[4], pr[1], pr[16], pr[13], pr[9], pr[5], pr[2], pr[17], pr[14],
            pr[10], pr[6]
            , pr[18], pr[15], pr[11])

        # 60 degree shift of tiles to represent 3rd line
        pr3 = (
            pr[16], pr[12], pr[7], pr[17], pr[13], pr[8], pr[3], pr[18], pr[14], pr[9], pr[4], pr[0], pr[16], pr[10],
            pr[5], pr[1]
            , pr[11], pr[6], pr[2])

        if rsrc_divsr_calc(pr, pr2, pr3) > tolerance:
            continue
        else:
            catan_map(pr,standard_map_shape)
            return rsrc_divsr_calc(pr, pr2, pr3)


print(rsrc_whole_calc(200))

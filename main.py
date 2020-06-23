from collections import Counter
from random import shuffle, randint
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import shapely.geometry as sg
import shapely.ops as so

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


def item_touches_calc(map_tiles):
    r = lambda: randint(0, 255)
    r1layout = [(0, 0), (1, 1), (1, 2), (0, 3), (0, 0)]
    r2layout = [(0, 0), (-1, 1), (-1, 2), (0, 3), (0, 0)]
    plot_start = ((0, 0), (2, 0), (4, 0),
                  (-1, -2), (1, -2), (3, -2), (5, -2),
                  (-2, -4), (0, -4), (2, -4), (4, -4), (6, -4),
                  (-1, -6), (1, -6), (3, -6), (5, -6),
                  (0, -8), (2, -8), (4, -8))

    def poly_adjust(layout, layout2, plotstartpoints):
        #fig, axs = plt.subplots()
        #axs.set_aspect('equal', 'datalim')
        output = []
        for y in plotstartpoints:
            temp, temp2 = [], []
            for xy in range(len(layout)):
                temp.append((layout[xy][0] + y[0], layout[xy][1] + y[1]))
                temp2.append((layout2[xy][0] + y[0], layout2[xy][1] + y[1]))
            r1 = sg.Polygon(temp)
            r2 = sg.Polygon(temp2)
            new_shape = so.cascaded_union([r1, r2])
            output.append(new_shape)
            #xs, ys = new_shape.exterior.xy
            #axs.fill(xs, ys, alpha=0.5, fc='#%02X%02X%02X' % (r(), r(), r()), ec='none')
        return output

    totalpoints_calc = poly_adjust(r1layout, r2layout, plot_start)
    #print(totalpoints_calc)
    #print(totalpoints_calc[0].touches(totalpoints_calc[2]))
    totalpoints=0

    for anum in range(len(totalpoints_calc)):
        for bnum in range(len(totalpoints_calc)):
            tch_tst = totalpoints_calc[anum].touches(totalpoints_calc[bnum])
            sm_tl_tst = map_tiles[anum] == map_tiles[bnum]
            if tch_tst and sm_tl_tst:
                totalpoints+=5
            else:
                pass
    print(totalpoints)
    return totalpoints


# [vertical coord,vertical coord,
def catan_map_generator(resource_layout, map_shape):
    map_tiles = []
    for item in range(len(resource_layout)):
        if resource_layout[item] == 'mountain':
            map_tiles.append(['Red', 'Mountain'])
        elif resource_layout[item] == 'field':
            map_tiles.append(['Yellow', 'Field'])
        elif resource_layout[item] == 'forest':
            map_tiles.append(['#254117', 'Forest '])
        elif resource_layout[item] == 'pasture':
            map_tiles.append(['#52D017', 'Pasture'])
        elif resource_layout[item] == 'hill':
            map_tiles.append(['Brown', 'Hills'])
        elif resource_layout[item] == 'desert':
            map_tiles.append(['White', 'Desert'])
        else:
            print(resource_layout[item])

    # Horizontal cartesian coords
    hcoord = [c[0] for c in map_shape]

    # Vertical cartersian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in map_shape]

    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    coords = []
    coords_shapes = []
    for x, y, c, l in zip(hcoord, vcoord, map_tiles, map_tiles):
        coords.append((x, y))
        color = c[0].lower()
        hex = RegularPolygon((x, y), numVertices=6, radius=4.043 / 7,
                             orientation=np.radians(60),
                             facecolor=color, alpha=0.2, edgecolor='k')
        g = ax.add_patch(hex)
        coords_shapes.append([str(ax.add_patch(hex))])
        ax.add_patch(hex)
        # Also add a text label
        ax.text(x, y + 0.2, l[1], ha='center', va='center', size=10)

    # Also add scatter points in hexagon centres
    ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in map_tiles], alpha=0.5)
    plt.show()
    return map_tiles


def rsrc_whole_calc(tol_rsrc_distrib,tol_same_tiles):
    # function combines multiple functions that determines if resource distribution and resource clustering is in acceptable
    # standards and if not, it reshuffles the board
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

        distribution_outcome = rsrc_divsr_calc(pr, pr2, pr3)
        distribution_boolean = distribution_outcome > tol_rsrc_distrib
        item_touches_outcome = item_touches_calc(pr)
        item_touches_boolean = item_touches_outcome > tol_same_tiles
        if item_touches_boolean and distribution_boolean:
            print(distribution_boolean, item_touches_boolean)
            catan_map_generator(pr, standard_map_shape)
            return
        else:
            continue


print(rsrc_whole_calc(200,30))

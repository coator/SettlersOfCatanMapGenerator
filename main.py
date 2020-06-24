# https://www.boardgameanalysis.com/what-is-a-balanced-catan-board/

from collections import Counter
from itertools import islice
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import shapely.geometry as sg
import shapely.ops as so

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


# a class I created that I have not used
# class pip:
#    def __init__(self, board_location, tile, value):
#        self.tile = tile
#        self.value = value
#        self.board_location = board_location


def rsrc_shfl():
    # Originally was planned so that if there were two resources near each other the resources will reshuffle, but since
    # I have implemented a system to reshuffle if resource_clustering is above threshold I have eliminated this feature
    pr = [
        'field', 'field', 'field', 'field', 'pasture', 'pasture', 'pasture', 'pasture', 'forest', 'forest', 'forest',
        'forest', 'hill', 'hill', 'hill', 'mountain', 'mountain', 'mountain', 'desert']
    shuffle(pr)
    #    item = 0
    # while item in range(len(pr) - 1):
    #    if pr[item] == pr[item + 1]:
    #        shuffle(pr)
    #        item = 0
    #    else:
    #        item += 1"""
    return tuple(pr)


def tile_resource_distribution(*argv):
    # Resource distribution is calculated by dividing the map into half 3 times, summing the difference of squares
    # on the two sides for each resource, each time the map is divided.
    total = 0
    for arg in argv:
        # print(arg)
        differences = Counter(arg[:7] * 6) + Counter(arg[8:12] * 3) - Counter(arg[13:] * 6) + Counter(arg[8:12] * 3)
        # var is squaring the difference amount
        total = + sum(x ** 2 for x in differences.values())
    # print(total)
    return total


def item_touches_calc(map_tiles):
    # tThis calculator uses shapely to build a Matplotlib map and then determines if the tiles are touching with a for
    # loop it is quite possible I will remove this later as I know have a list that does not change unless the board
    # changes
    # _______________________________________________________________
    # Originally I had functionality to generate the board since I was unsure how it would look but I have commented
    # that out

    # I had r = lambda: randint(0, 255)
    r1layout = [(0, 0), (1, 1), (1, 2), (0, 3), (0, 0)]
    r2layout = [(0, 0), (-1, 1), (-1, 2), (0, 3), (0, 0)]
    plot_start = ((0, 0), (2, 0), (4, 0),
                  (-1, -2), (1, -2), (3, -2), (5, -2),
                  (-2, -4), (0, -4), (2, -4), (4, -4), (6, -4),
                  (-1, -6), (1, -6), (3, -6), (5, -6),
                  (0, -8), (2, -8), (4, -8))

    def poly_adjust(layout, layout2, plotstartpoints):
        # fig, axs = plt.subplots()
        # axs.set_aspect('equal', 'datalim')
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
            # xs, ys = new_shape.exterior.xy
            # axs.fill(xs, ys, alpha=0.5, fc='#%02X%02X%02X' % (r(), r(), r()), ec='none')
        return output

    totalpoints_calc = poly_adjust(r1layout, r2layout, plot_start)
    # print(totalpoints_calc)
    # print(totalpoints_calc[0].touches(totalpoints_calc[2]))
    totalpoints = 0

    for anum in range(len(totalpoints_calc)):
        for bnum in range(len(totalpoints_calc)):
            tch_tst = totalpoints_calc[anum].touches(totalpoints_calc[bnum])
            sm_tl_tst = map_tiles[anum] == map_tiles[bnum]
            if tch_tst and sm_tl_tst:
                totalpoints += 5
            else:
                pass
    # print(totalpoints)
    return totalpoints


def catan_map_generator(resource_layout, map_shape):
    # generates the map once the parameters are acceptable.
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
            print(resource_layout[item], ' was not counted')

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


def pipvalue_distribution_per_resource(pv_dist_tol):
    while True:
        g = []
        pv = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        pv_dice_chance = [1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 4, 4, 3, 3, 2, 2, 1]
        tile_shfl = list(zip(pv, pv_dice_chance))
        shuffle(tile_shfl)
        length_to_split = [4, 4, 4, 3, 3]  # could be used for other combinations in expansions
        inp = iter(tile_shfl)
        out = [list(islice(inp, elem)) for elem in length_to_split]
        for x in out:
            expected = round(float(len(x) * 58 / 18), 3)
            actual = sum(x[1])
            g.append((expected - actual) ** 2)
        g = sum(g)
        if g > pv_dist_tol:
            pass
        else:
            tile_shfl.append((0, 0))
            ts_total = list(resource_split(tile_shfl))
            g = []
            for x in ts_total:
                for xx in x:
                    g.append(xx)
            tile_shfl = tile_shfl, list(g[0:19]), list(g[19:])
            pipvalue_distribution_board(tile_shfl)


def pipvalue_distribution_board(*argv):
    g = [0, 0]
    for arg in argv:
        for argitem in arg:
            g[0] = sum((Counter(argitem[:7][1]) + (Counter(argitem[8:12][1])) - \
                           Counter(argitem[13:][1]) + Counter(argitem[8:12][1])).values())
            g[1]=g[0]+g[1]
    g=g[1]
    print(g)
    return g



    #total = + sum(x ** 2 for x in differences.values())


def resource_split(board):
    board2 = (
        board[7], board[3], board[0], board[12], board[8], board[4], board[1], board[16], board[13], board[9],
        board[5], board[2], board[17], board[14], board[10], board[6], board[18], board[15], board[11])

    # 60 degree shift of tiles to represent 3rd line
    board3 = (
        board[16], board[12], board[7], board[17], board[13], board[8], board[3], board[18], board[14], board[9],
        board[4]
        , board[0], board[16], board[10], board[5], board[1], board[11], board[6], board[2])

    boardtotal = board2, board3
    return boardtotal


def rsrc_whole_calc(tol_rsrc_distrib, tol_same_tiles, pv_dist_tol_per_resource,tolerance_pip_distribution):
    # function combines multiple functions that determines if resource distribution and resource clustering is in acceptable
    # standards and if not, it reshuffles the board
    while True:
        # generates board
        pr = rsrc_shfl()

        #        # 30 degree shift of tiles to represent 2nd line
        #       pr2 = (
        #          pr[7], pr[3], pr[0], pr[12], pr[8], pr[4], pr[1], pr[16], pr[13], pr[9], pr[5], pr[2], pr[17], pr[14],
        #         pr[10], pr[6]
        #        , pr[18], pr[15], pr[11])
        #
        #       # 60 degree shift of tiles to represent 3rd line
        #      pr3 = (
        #         pr[16], pr[12], pr[7], pr[17], pr[13], pr[8], pr[3], pr[18], pr[14], pr[9], pr[4], pr[0], pr[16], pr[10],
        #        pr[5], pr[1]
        #       , pr[11], pr[6], pr[2])

        btotal = resource_split(pr)

        distribution_outcome = tile_resource_distribution(pr, btotal[0], btotal[1])
        distribution_boolean = distribution_outcome > tol_rsrc_distrib
        item_touches_outcome = item_touches_calc(pr)
        item_touches_boolean = item_touches_outcome > tol_same_tiles
        if item_touches_boolean and distribution_boolean:
            piplistlist = pipvalue_distribution_per_resource(pv_dist_tol_per_resource)
            return
        else:
            continue


rsrc_whole_calc(200, 30, 10,10)

import matplotlib.pyplot as pl
from matplotlib.gridspec import GridSpec
import numpy
from PIL import Image
import requests
import imgur_url
from io import BytesIO

pl.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
pl.rcParams['font.serif'] = ['Microsoft JhengHei']


def fig2img(fig):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data(fig)
    w, h, d = buf.shape
    return Image.frombytes("RGBA", (w, h), buf.tostring())


def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = numpy.fromstring(fig.canvas.tostring_argb(), dtype=numpy.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = numpy.roll(buf, 3, axis=2)
    return buf


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        pl.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom')


position2 = [[0, 0], [0, 1]]
position4 = [[0, 0], [0, 1], [1, 0], [1, 1]]
position6 = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
position9 = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
position12 = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3]]
position16 = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3], [3, 0],
              [3, 1], [3, 2], [3, 3]]
position20 = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2],
              [2, 3], [2, 4], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4]]
position25 = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2],
              [2, 3], [2, 4], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]


def drawing(inputlist):
    pictrueNumber = len(inputlist)
    if pictrueNumber == 1:
        figure = pl.figure(figsize=(5, 5))
        thegrid = GridSpec(1, 1)
        for inner in inputlist:
            ax = pl.subplot(thegrid[0, 0])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
    elif pictrueNumber <= 2:
        figure = pl.figure(figsize=(10, 5))
        thegrid = GridSpec(1, 2)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position2[position][0], position2[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    elif pictrueNumber <= 4:
        figure = pl.figure(figsize=(10, 10))
        thegrid = GridSpec(2, 2)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position4[position][0], position4[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    elif pictrueNumber <= 6:
        figure = pl.figure(figsize=(15, 10))
        thegrid = GridSpec(2, 3)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position6[position][0], position6[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    elif pictrueNumber <= 9:
        figure = pl.figure(figsize=(15, 15))
        thegrid = GridSpec(3, 3)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position9[position][0], position9[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    elif pictrueNumber <= 12:
        figure = pl.figure(figsize=(20, 15))
        thegrid = GridSpec(3, 4)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position12[position][0], position12[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    elif pictrueNumber <= 16:
        figure = pl.figure(figsize=(20, 20))
        thegrid = GridSpec(4, 4)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position16[position][0], position16[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    elif pictrueNumber <= 20:
        figure = pl.figure(figsize=(25, 20))
        thegrid = GridSpec(4, 5)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position20[position][0], position20[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    elif pictrueNumber <= 25:
        figure = pl.figure(figsize=(25, 25))
        thegrid = GridSpec(5, 5)
        position = 0
        for inner in inputlist:
            ax = pl.subplot(thegrid[position25[position][0], position25[position][1]])
            labels = []
            value = []
            for innerinner in inner:
                if innerinner is inner[0]:
                    ax.set_title(innerinner)
                else:
                    labels += [innerinner[0] + '\n' + innerinner[1]]
                    value += [int(innerinner[2])]
            width = 0.5
            rects1 = pl.bar(labels, value, width, color='r')
            autolabel(rects1)
            position += 1
    im = fig2img(figure)
    #im.show()
    pl.gcf().clear()
    return imgur_url.getUrl(im)



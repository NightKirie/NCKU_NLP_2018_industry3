#-*-coding:utf-8-*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
import matplotlib.font_manager as font_manager
from matplotlib.gridspec import GridSpec
import numpy
from PIL import Image
import requests
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


def drawing1_1(inputlist):
    inputlist1 = inputlist[0]
    inputlist2 = inputlist[1]
    inputlist3 = inputlist[2]
    figure = pl.figure()
    thegrid = GridSpec(1, 1)
    ax = pl.subplot(thegrid[0, 0])
    labels = [inputlist2[0] + "" +inputlist2[1], inputlist3[0] + "" + inputlist3[1]]
    value = [int(inputlist2[2]), int(inputlist3[2])]
    width = 0.5
    rects1 = pl.bar(labels, value, width, color='r')
    ax.set_title(inputlist1[2])
    autolabel(rects1)
    im = fig2img(figure)
    #im.show()
    pl.gcf().clear()
    return im


def drawing1_2(inputlist):
    print(inputlist)
    tb = prettytable.PrettyTable()
    tb.set_style(prettytable.MSWORD_FRIENDLY)
    tb.add_column("學校名稱",
                  ['科系名稱', "學生數", '教師數', '上學年度畢業生數', '106學年度新生註冊率', '畢業專業學分數', '畢業通識學分/共同學分數', '畢業實習學分數', '畢業其他學分數',
                   '畢業總學分數', '105第一學期休學人數', '105第二學期開設專業必修學分數', '105第二學期開設專業選修學分數', '106指考最低錄取分數'])
    for array in inputlist:
        tb.add_column(array[0], array[1:])
    print(tb.get_string())
    return tb.get_string()

def drawing2(inputlist):
    tb = prettytable.PrettyTable()
    tb.add_column("可能的目標校系", inputlist)
    print(tb.get_string())
    return tb.get_string()


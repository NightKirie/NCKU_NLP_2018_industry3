import matplotlib.pyplot as pl
from matplotlib.gridspec import GridSpec
import numpy
from PIL import Image
import requests
from io import BytesIO
# pl.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
# pl.rcParams['font.serif'] = ['Microsoft JhengHei']
'''
import matplotlib.font_manager as font_manager

path = "kaiu.ttf"
prop = font_manager.FontProperties(fname=path)
pl.rcParams['font.family'] = prop.get_name()
'''


'''
This is English version
file name: graphing.py
function bane: drawing
usage: graphing.drawing("input")

  input       return
     
師生數量      image
註冊率        string 
就業比例      image
學測分數      image
指考分數      string
'''


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


def drawing(string):
    if string == "師生數量":
        figure = pl.figure()
        thegrid = GridSpec(1, 1)
        pl.subplot(thegrid[0, 0])
        labels = 'student', 'Full-time teacher', 'Part-time teacher'
        value = [21252, 1326, 684]
        width = 0.5
        rects1 = pl.bar(labels, value, width, color='r')
        autolabel(rects1)
        im = fig2img(figure)
        #  im.show()
        pl.gcf().clear()
        return im
    elif string == "註冊率":
        array = [
            "              大學    碩士    碩專",
            "95學年度     95.64%  96.64%  98.38%",
            "96學年度     95.32%  95.38%  93.65%",
            "97學年度     97.24%  95.57%  93.08%",
            "98學年度     95.98%  96.94%  99.39%",
            "99學年度     96.01%  92.05%  95.23%",
            "100學年度    95.53%  95.59%  88.42%",
            "101學年度    95.72%  95.01%  88.00%",
            "102學年度    96.49%  93.89%  88.63%",
            "103學年度    95.05%  93.96%  87.98%",
            "104學年度    95.22%  92.67%  88.64%",
            "105學年度    95.31%  94.85%  93.11%",
            "106學年度    95.35%  95.32%  94.40%"
        ]
        outputstring = ""
        for each in array:
            outputstring += each + "\n"
        # print(outputstring)
        return outputstring
    elif string == "就業比例":
        figure = pl.figure()
        thegrid = GridSpec(2, 2)

        # labels = " ", "  ", "   ", "    ", "     "
        labels = "working", "military service", "studying", "find a job", "other"

        pl.subplot(thegrid[0, 0], aspect=1)
        value = [23.61, 3.76, 59.66, 5.71, 7.26]
        pl.pie(value, labels=labels, autopct='%1.1f%%', shadow=True)
        pl.title('Bachelor')

        pl.subplot(thegrid[0, 1], aspect=1)
        value = [71.54, 8.56, 5.67, 10.67, 3.56]
        pl.pie(value, labels=labels, autopct='%1.1f%%', shadow=True)
        pl.title('master')

        pl.subplot(thegrid[1, 0], aspect=1)
        value = [84.49, 8.02, 0.53, 6.95, 0]
        pl.pie(value, labels=labels, autopct='%1.1f%%', shadow=True)
        pl.title('doctor')

        im = fig2img(figure)
        # im.show()
        pl.gcf().clear()

        return im
    elif string == "學測分數":
        response = requests.get(
            "https://www.caac.ccu.edu.tw/cacportal/apply_his_report/106/106_sieve_standard/report/pict/004.png")
        im = Image.open(BytesIO(response.content))
        # im.show()
        return im
    elif string == "指考分數":
        array = [
            "中國文學系	            412.00",
            "外國語文學系	        497.55",
            "歷史學系	            379.15",
            "台灣文學系	            504.80",
            "數學系	                365.45",
            "物理學系	            429.25",
            "化學系	                428.35",
            "地球科學系	            334.50",
            "光電科學與工程學系	    364.50",
            "機械工程學系	        356.30",
            "化學工程學系	        360.70",
            "材料科學及工程學系	    370.40",
            "資源工程學系	        342.00",
            "土木工程學系	        346.80",
            "水利及海洋工程學系	    440.50",
            "工程科學系	            356.20",
            "系統及船舶機電工程學系	347.80",
            "航空太空工程學系	    355.50",
            "環境工程學系	        345.70",
            "測量及空間資訊學系	    336.60",
            "生物醫學工程學系	    357.10",
            "工業與資訊管理學系	    351.30",
            "交通管理科學系	        339.40",
            "企業管理學系	        238.00",
            "統計學系	            276.55",
            "會計學系	            572.50",
            "醫學系(自費)	        442.90",
            "醫學系(公費)	        423.40",
            "醫學檢驗生物技術學系	420.60",
            "護理學系	            363.33",
            "職能治療學系	        370.70",
            "物理治療學系	        392.18",
            "藥學系	                414.85",
            "政治學系	            422.55",
            "經濟學系	            443.30",
            "法律學系	            399.20",
            "心理學系	            418.05",
            "電機工程學系	        385.50",
            "資訊工程學系	        376.80",
            "建築學系	            431.43",
            "都市計劃學系	        433.00",
            "工業設計學系	        428.05",
            "生命科學系	            451.53",
            "生物科技與產業科學系	447.85",
            "大一全校不分系學士學位學程	382.00"
        ]
        outputstring = ""
        for each in array:
            outputstring += each + "\n"
        # print(outputstring)
        return outputstring

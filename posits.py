""" Positions sets. """
import sys
from time import perf_counter
from typing import Union
import cv2
import numpy


def print_info(msg: str) -> None:
    """
        @brief Print information.
        This function is only use for posits.py(posits). 
        @param msg The message need to print. 
    """
    print("POSIT-LOAD: " + msg)


def print_errs(msg: str) -> None:
    """
        @brief Print errors. 
        This function is only use for posits.py(posits). 
        @param msg The message need to print. 
    """
    print("POSIT-LOAD: " + msg)


def print_scroll(start_time_perf_counter: float, all: Union[int, float], now: Union[int, float], length: int = 50):
    time = perf_counter() - start_time_perf_counter
    time = int(time)
    hour = time // 3600
    minute = time % 3600 // 60
    second = time % 60
    timestr = str(hour).zfill(1) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
    print(
        "|" + "-" * int(length / 100 * int(now / all * 100)) + "|" + str(int(now / all * 100)) + "% " + timestr + "\r",
        end='')

print_info("Loading ...")

# TODO:初始化数据
try:
    COLORS = {
        "湖北": (133, 133, 208),
        "湖南": (0, 168, 243),
        "河北": (255, 210, 225),
        "河南": (203, 124, 124),
        "广西": (190, 33, 15),
        "广东": (0, 0, 0),
        "内蒙古": (14, 209, 69),
        "新疆": (255, 242, 0),
        "西藏": (184, 61, 186),
        "宁夏": (136, 0, 27),
        "福建": (129, 156, 173),
        "吉林": (162, 82, 157),
        "安徽": (211, 200, 248),
        "浙江": (151, 209, 246),
        "云南": (216, 227, 228),
        "贵州": (255, 202, 24),
        "辽宁": (116, 91, 118),
        "黑龙江": (241, 114, 250),
        "四川": (97, 109, 169),
        "青海": (140, 255, 251),
        "甘肃": (255, 127, 39),
        "山西": (220, 186, 186),
        "陕西": (88, 88, 88),
        "山东": (1, 171, 157),
        "海南": (63, 72, 204),
        "台湾": (196, 255, 14),
        "香港": (255, 174, 200),
        "澳门": (90, 49, 127),
        "江苏": (133, 246, 186),
        "北京": (236, 28, 36),
        "天津": (177, 162, 92),
        "上海": (192, 153, 94),
        "重庆": (82, 39, 34),
        "江西": (252, 121, 121)
    }
    AREAS_L = list(COLORS.keys())
    COLORS_L = []
    for key in COLORS:
        COLORS_L.append(COLORS[key])
    POS = {
        "湖北": [],
        "湖南": [],
        "河北": [],
        "河南": [],
        "广西": [],
        "广东": [],
        "内蒙古": [],
        "新疆": [],
        "西藏": [],
        "宁夏": [],
        "福建": [],
        "吉林": [],
        "安徽": [],
        "浙江": [],
        "云南": [],
        "贵州": [],
        "辽宁": [],
        "黑龙江": [],
        "四川": [],
        "青海": [],
        "甘肃": [],
        "山西": [],
        "陕西": [],
        "山东": [],
        "海南": [],
        "台湾": [],
        "香港": [],
        "澳门": [],
        "江苏": [],
        "北京": [],
        "天津": [],
        "上海": [],
        "重庆": [],
        "江西": [],
    }
    TEXTS_POS = {
        "新疆": (127, 140),
        "西藏": (140, 238),
        "青海": (210, 190),
        "甘肃": (271, 202),
        "内蒙古": (361, 110),
        "宁夏": (282, 180),
        "陕西": (299, 211),
        "四川": (256, 241),
        "云南": (245, 302),
        "贵州": (290, 280),
        "广西": (306, 309),
        "重庆": (296, 250),
        "湖南": (328, 265),
        "广东": (348, 304),
        "澳门": (349, 334),
        "香港": (368, 323),
        "湖北": (333, 235),
        "江西": (362, 262),
        "福建": (384, 279),
        "浙江": (396, 250),
        "安徽": (373, 233),
        "江苏": (393, 221),
        "上海": (424, 230),
        "河南": (339, 209),
        "山东": (371, 183),
        "山西": (325, 178),
        "河北": (351, 165),
        "北京": (360, 135),
        "天津": (382, 159),
        "辽宁": (400, 126),
        "吉林": (413, 99),
        "黑龙江": (421, 69),
        "台湾": (435, 301),
        "海南": (341, 352)
    }
    SPEC_STATIC = [
        "上海",
        "香港",
        "澳门",
        "海南",
        "台湾",
        "天津"
    ]
    SPEC_HONGKONG = []
    SPEC_MACAO = []
    START = perf_counter()
    pic = cv2.imread("map_colored.png")
    hongkong = cv2.imread("map_hongkong.png")
    macao = cv2.imread("map_macao_2.png")
    array = numpy.array(pic)
    hongkongarr = numpy.array(hongkong)
    macaoarr = numpy.array(macao)
    cnt = 0
    for row in range(383):
        for step in range(50):
            for col in range(step * 12, step * 12 + 12):
                clr = array[row][col]
                new_clr = (clr[2], clr[1], clr[0])
                if new_clr in list(COLORS_L):
                    index = list(COLORS_L).index(new_clr)
                    POS[list(AREAS_L)[index]].append([col, row])
                cnt += 1
                if cnt % 2500 == 0:
                    print_scroll(START, 271020, cnt, 40)
    for row in range(72):
        for col in range(110):
            clr = hongkongarr[row][col]
            new_clr = (clr[2], clr[1], clr[0])
            if new_clr == (238, 188, 125):
                SPEC_HONGKONG.append([col, row])
            cnt += 1
            if cnt % 2500 == 0:
                print_scroll(START, 271020, cnt, 40)
    for row in range(222):
        for col in range(150):
            clr = macaoarr[row][col]
            new_clr = (clr[2], clr[1], clr[0])
            if new_clr == (235, 243, 121):
                SPEC_MACAO.append([col, row])
            cnt += 1
            if cnt % 2500 == 0 or cnt == 271020:
                print_scroll(START, 271020, cnt, 40)
    # TODO:结束
    print()
    print_info("POSIT-LOAD: Done. ")
    del [
        START,
        array,
        clr,
        cnt,
        col,
        hongkong,
        hongkongarr,
        index,
        key,
        macao,
        macaoarr,
        new_clr,
        pic,
        row,
        step
    ]
except Exception as e:
    print_errs(str(e))
    sys.exit()

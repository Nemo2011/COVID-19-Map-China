""" The main program of the map. """
import importlib
from PIL import Image, ImageDraw, ImageFont
import numpy
import cv2
from typing import Union
import sys
from time import perf_counter

START = perf_counter()


def print_info(msg: str) -> None:
    """
        @brief Print information.
        @param msg The message need to print.
    """
    prtstr = str(int(round(float(perf_counter() - START), 4)
                 * 10000)).zfill(5) + " INFO: " + msg
    print(prtstr)


def print_errs(msg: str) -> None:
    """
        @brief Print errors.
        @param msg The message need to print.
    """
    prtstr = str(int(round(float(perf_counter() - START), 4)
                 * 10000)).zfill(5) + " ERRS: " + msg
    print(prtstr)


def paint_chinese_opencv(im: object, chinese: str, pos: Union[tuple, list], color: Union[tuple, list],
                         size: Union[int, float]):
    """
        @brief Drawing chinese on opencv drawing map.
        Need simsun.ttc.
        @param im Image in cv2.
        @param chinese The text.
        @param pos Position of x, y.
        @param color RGB color of the text.
        @param size The size of the text.
    """
    img_pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    local = "simsun.ttc"
    font = ImageFont.truetype(local, size, encoding="utf-8")
    fillColor = color
    position = pos
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, chinese, font=font, fill=tuple(fillColor))
    img = cv2.cvtColor(numpy.asarray(img_pil), cv2.COLOR_RGB2BGR)
    return img


def number2str_with_sum_or_sub(num: int) -> str:
    """
        @brief Return a string of an number that has + and -.
        For example:
        ``` python
        >>> number2str_with_sum_or_sub(1)
        '+1'
        >>> number2str_with_sum_or_sub(-3)
        '-1'
        >>> number2str_with_sum_or_sub(0)
        '+0'
        ```
        @param num The number that need to return the string result.
    """
    if num >= 0:
        return '+' + str(num)
    else:
        return str(num)


def color_by_num(num: int, level: bool = False) -> Union[tuple, list]:
    """
        @brief Return a color's RGB set of a red by a number.
        LEVEL1:(222, 31, 5)    > 10000
        LEVEL2:(255, 39, 54)   1000 ~ 9999
        LEVEL3:(255, 99, 65)   500 ~ 999
        LEVEL4:(255, 165, 119) 100 ~ 499
        LEVEL5:(255, 206, 160) 10 ~ 99
        LEVEL6:(255, 231, 178) 1 ~ 9
        LEVEL7:(255, 255, 255) 0
        @param num The number need to push in.
        @param level Return the level.
    """
    if not level:
        if num > 10000:
            return 222, 31, 5
        elif num > 999:
            return 255, 39, 54
        elif num > 499:
            return 255, 99, 65
        elif num > 99:
            return 255, 165, 119
        elif num > 9:
            return 255, 206, 160
        elif num > 0:
            return 255, 231, 178
        else:
            return 255, 255, 255
    else:
        if num > 10000:
            return 222, 31, 5, 1
        elif num > 999:
            return 255, 39, 54, 2
        elif num > 499:
            return 255, 99, 65, 3
        elif num > 99:
            return 255, 165, 119, 4
        elif num > 9:
            return 255, 206, 160, 5
        elif num > 0:
            return 255, 231, 178, 6
        else:
            return 255, 255, 255, 7


def color_by_level(level: int) -> Union[tuple, list]:
    """
        @brief Return a color's RGB set of a red by a level.
        LEVEL1:(222, 031, 005)
        LEVEL2:(255, 039, 054)
        LEVEL3:(255, 099, 065)
        LEVEL4:(255, 165, 119)
        LEVEL5:(255, 206, 160)
        LEVEL6:(255, 231, 178)
        LEVEL7:(255, 255, 255)
        @param level The input level.
    """
    if level == 1:
        return 222, 31, 5
    elif level == 2:
        return 255, 39, 54
    elif level == 3:
        return 255, 99, 65
    elif level == 4:
        return 255, 165, 119
    elif level == 5:
        return 255, 206, 160
    elif level == 6:
        return 255, 231, 178
    elif level == 7:
        return 255, 255, 255


def range_by_level(level: int) -> str:
    """
        @brief Return a color's RGB set of a red by a number.
        LEVEL1: > 10000
        LEVEL2: 1000 ~ 9999
        LEVEL3: 500 ~ 999
        LEVEL4: 100 ~ 499
        LEVEL5: 10 ~ 99
        LEVEL6: 1 ~ 9
        LEVEL7: 0
        @param level The input level.
    """
    if level == 1:
        return "> 10000"
    elif level == 2:
        return "1000 ~ 9999"
    elif level == 3:
        return "500 ~ 999"
    elif level == 4:
        return "100 ~ 499"
    elif level == 5:
        return "10 ~ 99"
    elif level == 6:
        return "1 ~ 9"
    elif level == 7:
        return "0"


def spec_append(lst: Union[tuple, list], obj: object):
    """
    @brief Append a value to a list.
    If you use append, the copy() will not do successfully, two lists in two dicts will be same.
    The solution is reset the list in the copied dict, then the first dict and the copied dict will not same.
    So there we need to write a function by ourselves.
    @param lst The list value.
    @param obj The object to append.
    """
    new_lst = []
    for lstobj in lst:
        new_lst.append(lstobj)
    new_lst.append(obj)
    return new_lst


def num_or_none(num: int) -> str:
    """
    @brief Return a number string of a number. If the number is 0 then return '-'.
    For example:
    ``` python
    >>> num_or_none(1)
    '1'
    >>> num_or_none(-5)
    '-5'
    >>> num_or_none(0)
    '-'
    ```
    """
    if num == 0:
        return "-"
    else:
        return str(num)


if __name__ == '__main__':
    try:
        # TODO:检查版本
        print_info("Checking python version. ")
        ver = sys.version_info
        print_info("Python version: " + str(tuple(ver)[0:3]))
        if ver < (3, 6, 0):
            print_errs(
                "Your python version is too old. Please update to Python 3.6.0")
            sys.exit()

        # TODO:初始化
        MAJOR = 1
        MINOR = 2
        MICRO = 0
        VER = str(MAJOR) + '.' + str(MINOR) + '.' + str(MICRO)
        DATE = '2022-03-21'
        print_info("COVID-19-Map-China: version " + VER)
        print_info("COVID-19-Map-China: last update at " + DATE)
        print_info("Loading COVID-19 datas. ")
        import covids
        from covids import (ADD_SORT, AREAS_SORT, CHINA_DEAD, CHINA_HEAL,
                            CHINA_IMPORT, CHINA_LOCAL, CHINA_NO_INFECT,
                            CHINA_NOW_CONFIRM, CHINA_SEVERE, CHINA_SUSPECT,
                            CHINA_TOTAL, CITIES, NOW_SORT, CONFIRM_SORT,
                            DEAD_SORT, GRADES, HEAL_SORT, LOCAL_SORT, TIME,
                            NOT_UPDATE_PROVINCE, NOT_UPDATE_CITIES)

        print_info("Done. ")
        print_info("Loading positions datas. ")
        from posits import POS, TEXTS_POS, SPEC_STATIC, SPEC_HONGKONG, SPEC_MACAO

        print_info("Done. ")
        print_info("Staring: ")
        cv2.namedWindow('COVID-19 Map of China', 0)
        cap = 'COVID-19-Map-China version ' + VER + ' on ' + DATE
        cv2.setWindowTitle('COVID-19 Map of China', cap)
        cv2.resizeWindow('COVID-19 Map of China', 785, 500)
        # 这些为页面设置
        select = ""
        showmode = 0
        point = [0, 0]
        evt = 0
        select_asked = False
        select_asked_select = ""
        cities_view = False
        page = 1
        down = False
        hides = [False, False, False, False, False, False, False, False]
        highlights = [False, False, False, False, False, False, False, False]
        down_count = 0

        while True:
            # TODO:绘制显示内容
            frame = cv2.imread("map_background.png")
            frame = paint_chinese_opencv(
                frame, "Update at: " + TIME, (250, 368), (0, 0, 0), 15)
            if not cities_view:
                frame = paint_chinese_opencv(
                    frame, "中国疫情\n  地图", (470, 10), (0, 0, 0), 30)
                for level in range(1, 8, 1):
                    color = color_by_level(level)
                    color = (color[2], color[1], color[0])
                    if hides[level] == True:
                        color = (125, 125, 125)
                    elif highlights[level] == True:
                        color = (253, 255, 199)
                    frame = paint_chinese_opencv(frame, range_by_level(
                        level), (10, level * 20 - 20), (0, 0, 0), 20)
                    img_pil = Image.fromarray(frame)
                    img_draw = ImageDraw.Draw(img_pil)
                    img_draw.rectangle(
                        ((0, level * 20 - 20), (8, level * 20)), fill=color)
                    img_draw.line(((8, 0), (8, 140)), fill=(0, 0, 0))
                    img_draw.line(((0, 140), (8, 140)), fill=(0, 0, 0))
                    frame = numpy.array(img_pil)
                if showmode == 0:
                    cv2.rectangle(frame, (95, 348), (95, 348), (255, 0, 0), 50)
                    cv2.rectangle(frame, (215, 348), (215, 348), (0, 0, 0), 50)
                    img_pil = Image.fromarray(frame)
                    img_draw = ImageDraw.Draw(img_pil)
                    img_draw.rectangle(
                        ((95, 323), (125, 373)), fill=(255, 0, 0))
                    img_draw.rectangle(
                        ((125, 323), (185, 373)), fill=(0, 0, 0))
                    img_draw.rectangle(
                        ((185, 323), (215, 373)), fill=(0, 0, 0))
                    frame = numpy.array(img_pil)
                    frame = paint_chinese_opencv(
                        frame, "现有", (80, 338), (255, 255, 255), 20)
                    frame = paint_chinese_opencv(
                        frame, "累计", (135, 338), (255, 255, 255), 20)
                    frame = paint_chinese_opencv(
                        frame, "新增", (190, 338), (255, 255, 255), 20)
                elif showmode == 1:
                    cv2.rectangle(frame, (95, 348), (95, 348), (0, 0, 0), 50)
                    cv2.rectangle(frame, (215, 348), (215, 348), (0, 0, 0), 50)
                    img_pil = Image.fromarray(frame)
                    img_draw = ImageDraw.Draw(img_pil)
                    img_draw.rectangle(((95, 323), (125, 373)), fill=(0, 0, 0))
                    img_draw.rectangle(
                        ((125, 323), (185, 373)), fill=(255, 0, 0))
                    img_draw.rectangle(
                        ((185, 323), (215, 373)), fill=(0, 0, 0))
                    frame = numpy.array(img_pil)
                    frame = paint_chinese_opencv(
                        frame, "现有", (80, 338), (255, 255, 255), 20)
                    frame = paint_chinese_opencv(
                        frame, "累计", (135, 338), (255, 255, 255), 20)
                    frame = paint_chinese_opencv(
                        frame, "新增", (190, 338), (255, 255, 255), 20)
                else:
                    cv2.rectangle(frame, (95, 348), (95, 348), (0, 0, 0), 50)
                    cv2.rectangle(frame, (215, 348),
                                  (215, 348), (255, 0, 0), 50)
                    img_pil = Image.fromarray(frame)
                    img_draw = ImageDraw.Draw(img_pil)
                    img_draw.rectangle(((95, 323), (125, 373)), fill=(0, 0, 0))
                    img_draw.rectangle(
                        ((125, 323), (185, 373)), fill=(0, 0, 0))
                    img_draw.rectangle(
                        ((185, 323), (215, 373)), fill=(255, 0, 0))
                    frame = numpy.array(img_pil)
                    frame = paint_chinese_opencv(
                        frame, "现有", (80, 338), (255, 255, 255), 20)
                    frame = paint_chinese_opencv(
                        frame, "累计", (135, 338), (255, 255, 255), 20)
                    frame = paint_chinese_opencv(
                        frame, "新增", (190, 338), (255, 255, 255), 20)
                if not select_asked:
                    confirm = f"累计确诊\n{CHINA_TOTAL[0]}\n{number2str_with_sum_or_sub(CHINA_TOTAL[1])}"
                    nowconfirm = f"现有确诊\n{CHINA_NOW_CONFIRM[0]}\n{number2str_with_sum_or_sub(CHINA_NOW_CONFIRM[1])}"
                    local = f"本土确诊\n{CHINA_LOCAL[0]}\n{number2str_with_sum_or_sub(CHINA_LOCAL[1])}"
                    imported = f"海外输入\n{CHINA_IMPORT[0]}\n{number2str_with_sum_or_sub(CHINA_IMPORT[1])}"
                    no_infect = f" 无症状\n{CHINA_NO_INFECT[0]}\n{number2str_with_sum_or_sub(CHINA_NO_INFECT[1])}"
                    severe = f"重症病例\n{CHINA_SEVERE[0]}\n{number2str_with_sum_or_sub(CHINA_SEVERE[1])}"
                    suspect = f"疑似病例\n{CHINA_SUSPECT[0]}\n{number2str_with_sum_or_sub(CHINA_SUSPECT[1])}"
                    heal = f" 已治愈\n{CHINA_HEAL[0]}\n{number2str_with_sum_or_sub(CHINA_HEAL[1])}"
                    dead = f"死亡病例\n{CHINA_DEAD[0]}\n{number2str_with_sum_or_sub(CHINA_DEAD[1])}"
                    frame = paint_chinese_opencv(
                        frame, confirm, (477, 85), (139, 0, 0), 12)
                    frame = paint_chinese_opencv(
                        frame, nowconfirm, (537, 85), (240, 0, 240), 12)
                    frame = paint_chinese_opencv(
                        frame, local, (477, 145), (139, 69, 19), 12)
                    frame = paint_chinese_opencv(
                        frame, imported, (537, 145), (0, 0, 139), 12)
                    frame = paint_chinese_opencv(
                        frame, no_infect, (477, 205), (125, 125, 125), 12)
                    frame = paint_chinese_opencv(
                        frame, severe, (537, 205), (139, 0, 0), 12)
                    frame = paint_chinese_opencv(
                        frame, suspect, (477, 265), (238, 197, 145), 12)
                    frame = paint_chinese_opencv(
                        frame, heal, (537, 265), (0, 139, 0), 12)
                    frame = paint_chinese_opencv(
                        frame, dead, (507, 325), (125, 125, 125), 12)
                    cv2.rectangle(frame, (475, 80), (525, 130), (0, 0, 139), 2)
                    cv2.rectangle(frame, (535, 80),
                                  (585, 130), (240, 0, 240), 2)
                    cv2.rectangle(frame, (475, 140),
                                  (525, 190), (19, 69, 139), 2)
                    cv2.rectangle(frame, (535, 140),
                                  (585, 190), (139, 0, 0), 2)
                    cv2.rectangle(frame, (475, 200), (525, 250),
                                  (125, 125, 125), 2)
                    cv2.rectangle(frame, (535, 200),
                                  (585, 250), (0, 0, 139), 2)
                    cv2.rectangle(frame, (475, 260), (525, 310),
                                  (145, 197, 238), 2)
                    cv2.rectangle(frame, (535, 260),
                                  (585, 310), (0, 139, 0), 2)
                    cv2.rectangle(frame, (505, 320), (555, 370),
                                  (125, 125, 125), 2)
                else:
                    area = select
                    add = ADD_SORT[AREAS_SORT.index(area)]
                    now = NOW_SORT[AREAS_SORT.index(area)]
                    confirm = CONFIRM_SORT[AREAS_SORT.index(area)]
                    cv2.rectangle(frame, (475, 150),
                                  (525, 200), (240, 0, 240), 2)
                    cv2.rectangle(frame, (535, 150),
                                  (585, 200), (0, 0, 139), 2)
                    cv2.rectangle(frame, (505, 210),
                                  (555, 260), (19, 69, 139), 2)
                    nowstr = f"现有病例\n{now}"
                    confirmstr = f"累计确诊\n{confirm}\n{number2str_with_sum_or_sub(add)}"
                    localstr = f"本土确诊\n{LOCAL_SORT[AREAS_SORT.index(area)]}"
                    left = (100 - len(area) * 25) / 2
                    frame = paint_chinese_opencv(
                        frame, area, (475 + left, 90), (0, 0, 139), 30)
                    cv2.rectangle(frame, (480, 290), (580, 330), (0, 0, 0), 2)
                    frame = paint_chinese_opencv(
                        frame, nowstr, (477, 155), (240, 0, 240), 12)
                    frame = paint_chinese_opencv(
                        frame, confirmstr, (537, 155), (139, 0, 0), 12)
                    frame = paint_chinese_opencv(
                        frame, localstr, (507, 215), (139, 69, 19), 12)
                    frame = paint_chinese_opencv(
                        frame, " 详细信息", (480, 300), (0, 0, 0), 20)
                    isupdate = not area in NOT_UPDATE_PROVINCE
                    if isupdate:
                        update_color = (0, 139, 0)
                        update_text = "已更新"
                    else:
                        update_color = (139, 0, 0)
                        update_text = "未更新"
                    frame = paint_chinese_opencv(
                        frame, update_text, (500, 350), update_color, 20)
                for idx, area in enumerate(POS):
                    for pos in POS[area]:
                        if not select == area:
                            if showmode == 0:
                                numselect = NOW_SORT[AREAS_SORT.index(area)]
                            elif showmode == 1:
                                numselect = CONFIRM_SORT[AREAS_SORT.index(
                                    area)]
                            else:
                                numselect = ADD_SORT[AREAS_SORT.index(area)]
                            color = color_by_num(numselect, level=True)
                            lvl = color[3]
                            color = [color[2], color[1], color[0]]
                            if hides[lvl] == True:
                                cv2.rectangle(frame, pos, pos,
                                              (125, 125, 125), thickness=1)
                            elif highlights[lvl] == True:
                                cv2.rectangle(frame, pos, pos,
                                              (253, 255, 199), thickness=1)
                            else:
                                cv2.rectangle(frame, pos, pos,
                                              color, thickness=1)
                        else:
                            cv2.rectangle(frame, pos, pos, [
                                          253, 255, 199], thickness=1)
                        if select_asked and select_asked_select == area:
                            cv2.rectangle(frame, pos, pos, [
                                          253, 255, 199], thickness=1)
                for idx, area in enumerate(TEXTS_POS):
                    if showmode == 0:
                        numselect = NOW_SORT[AREAS_SORT.index(area)]
                    elif showmode == 1:
                        numselect = CONFIRM_SORT[AREAS_SORT.index(area)]
                    else:
                        numselect = ADD_SORT[AREAS_SORT.index(area)]
                    level = color_by_num(numselect, level=True)[3]
                    if hides[level] == False and highlights[level] == False:
                        if area == "北京":
                            if showmode == 0:
                                numselect = NOW_SORT[AREAS_SORT.index('河北')]
                            else:
                                numselect = CONFIRM_SORT[AREAS_SORT.index(
                                    '河北')]
                            level = color_by_num(numselect, level=True)[3]
                            if level in [1,
                                         2] and not "河北" in SPEC_STATIC and "河北" != select and "河北" != select_asked_select:
                                frame = paint_chinese_opencv(
                                    frame, area, TEXTS_POS[area], (255, 255, 255), 12)
                            else:
                                frame = paint_chinese_opencv(
                                    frame, area, TEXTS_POS[area], (0, 0, 0), 12)
                        elif level in [1, 2] and not area in SPEC_STATIC and area != select and area != select_asked_select:
                            frame = paint_chinese_opencv(
                                frame, area, TEXTS_POS[area], (255, 255, 255), 12)
                        else:
                            frame = paint_chinese_opencv(
                                frame, area, TEXTS_POS[area], (0, 0, 0), 12)
                    else:
                        frame = paint_chinese_opencv(
                            frame, area, TEXTS_POS[area], (0, 0, 0), 12)
            else:
                cv2.rectangle(frame, (0, 0), (600, 383),
                              (255, 255, 255), thickness=600)
                cv2.rectangle(frame, (95, 348), (95, 348), (0, 0, 0), 50)
                cv2.line(frame, (0, 40), (600, 40), (0, 0, 0), 4)
                cv2.line(frame, (300, 40), (300, 383), (0, 0, 0), 4)
                if len(CITIES[select]) - page * 5 >= 0:
                    cityrange = list(range(0, len(CITIES[select])))[
                        (page - 1) * 5:page * 5]
                else:
                    cityrange = list(range(0, len(CITIES[select])))[
                        (page - 1) * 5:len(CITIES[select])]
                select_lst = [CONFIRM_SORT[AREAS_SORT.index(select)], NOW_SORT[AREAS_SORT.index(select)],
                              ADD_SORT[AREAS_SORT.index(
                                  select)], DEAD_SORT[AREAS_SORT.index(select)],
                              HEAL_SORT[AREAS_SORT.index(select)], LOCAL_SORT[AREAS_SORT.index(select)]]
                citylst = [{f"{select}所有": select_lst}]
                for index, key in enumerate(CITIES[select]):
                    if index in cityrange:
                        citylst.append({key: CITIES[select][key]})
                frame = paint_chinese_opencv(
                    frame, "返回", (76, 338), (255, 255, 255), 20)
                area = select
                if area == "香港":
                    positions = SPEC_HONGKONG
                elif area == "澳门":
                    positions = SPEC_MACAO
                else:
                    positions = POS[area][:]
                maxx = 0
                minx = 1000
                maxy = 0
                miny = 1000
                for apoint in positions:
                    if apoint[0] > maxx:
                        maxx = apoint[0]
                    if apoint[0] < minx:
                        minx = apoint[0]
                    if apoint[1] > maxy:
                        maxy = apoint[1]
                    if apoint[1] < miny:
                        miny = apoint[1]
                pweight = maxx - minx
                xobjpos = int((300 - pweight) / 2)
                leftmove = minx - xobjpos
                ptall = maxy - miny
                yobjpos = int((383 - ptall) / 2)
                upmove = miny - yobjpos
                for index, apoint in enumerate(positions):
                    positions[index] = [positions[index][0] -
                                        leftmove, positions[index][1] - upmove]
                frame = paint_chinese_opencv(
                    frame, select, (265, 0), (0, 0, 0), 30)
                frame = paint_chinese_opencv(
                    frame, "绿色为已更新", (525, 0), (0, 139, 0), 12)
                frame = paint_chinese_opencv(
                    frame, "红色为未更新", (525, 20), (139, 0, 0), 12)
                for pos in positions:
                    try:
                        xbig = int(280 / pweight)
                    except:
                        xbig = 100
                    ybig = int(200 / ptall)
                    final = min(xbig, ybig)
                    if final == 0:
                        final = 0.9
                    if final == 1:
                        final = 1.5
                    if final > 9:
                        final = 9
                    newpos = [pos[0] * final, pos[1] * final]
                    newweight = pweight * final + final * 2
                    newtall = ptall * final + final * 2
                    nxobjpos = (300 - newweight - final * 2) / 2
                    nyobjpos = (383 - newtall - final * 2) / 2
                    needminusx = xobjpos * final - nxobjpos
                    needminusy = yobjpos * final - nyobjpos
                    newpos = [newpos[0] - needminusx, newpos[1] - needminusy]
                    newpos = [int(newpos[0]), int(newpos[1])]
                    cv2.rectangle(frame, newpos, newpos,
                                  (0, 0, 0), int(final * 2))
                cv2.line(frame, (375, 40), (375, 285), (0, 0, 0), 2)
                cv2.line(frame, (420, 40), (420, 285), (0, 0, 0), 2)
                cv2.line(frame, (465, 40), (465, 285), (0, 0, 0), 2)
                cv2.line(frame, (510, 40), (510, 285), (0, 0, 0), 2)
                cv2.line(frame, (555, 40), (555, 285), (0, 0, 0), 2)
                cv2.line(frame, (300, 285), (600, 285), (0, 0, 0), 4)
                frame = paint_chinese_opencv(
                    frame, "城市", (305, 45), (0, 0, 0), 15)
                frame = paint_chinese_opencv(
                    frame, "确诊", (380, 45), (0, 0, 0), 15)
                frame = paint_chinese_opencv(
                    frame, "现有", (425, 45), (0, 0, 0), 15)
                frame = paint_chinese_opencv(
                    frame, "新增", (470, 45), (0, 0, 0), 15)
                frame = paint_chinese_opencv(
                    frame, "死亡", (515, 45), (0, 0, 0), 15)
                frame = paint_chinese_opencv(
                    frame, "治愈", (560, 45), (0, 0, 0), 15)
                cv2.line(frame, (300, 75), (600, 75), (0, 0, 0), 4)
                cv2.line(frame, (300, 105), (600, 105), (0, 0, 0), 2)
                cv2.line(frame, (300, 140), (600, 140), (0, 0, 0), 2)
                cv2.line(frame, (300, 175), (600, 175), (0, 0, 0), 2)
                cv2.line(frame, (300, 210), (600, 210), (0, 0, 0), 2)
                cv2.line(frame, (300, 245), (600, 245), (0, 0, 0), 2)
                cv2.rectangle(frame, (350, 335), (350, 335),
                              (125, 125, 125), 50)
                cv2.rectangle(frame, (550, 335), (550, 335),
                              (125, 125, 125), 50)
                frame = paint_chinese_opencv(frame,
                                             f"{page}/{int(len(CITIES[select]) / 5) + int(bool(len(CITIES[select]) % 5 / 1))}",
                                             (440, 326), (0, 0, 0), 20)
                frame = paint_chinese_opencv(
                    frame, "<-", (340, 326), (0, 0, 0), 20)
                frame = paint_chinese_opencv(
                    frame, "->", (540, 326), (0, 0, 0), 20)
                for index, city in enumerate(citylst):
                    y = 75 + 35 * index + 8
                    yfir = 75 + 35 * index + 8
                    citytxt = list(city.keys())[0]
                    if index == 0:
                        yfir = 85
                    if list(city.keys())[0] in list(GRADES[select].keys()) and index != 0:
                        yfir -= 8
                        frame = paint_chinese_opencv(frame, f"{GRADES[select][list(city.keys())[0]]}", (303, y + 8),
                                                     (0, 0, 139), 12)
                    addtxt = f"{num_or_none(city[list(city.keys())[0]][2])}"
                    if list(city.keys())[0].count("待确认") >= 1:
                        fircolor = (0, 0, 139)
                    else:
                        if list(city.keys())[0] in NOT_UPDATE_CITIES[select]:
                            fircolor = (139, 0, 0)
                        else:
                            fircolor = (0, 139, 0)
                    if index == 0:
                        frame = paint_chinese_opencv(
                            frame, citytxt, (303, yfir), (0, 0, 139), 12)
                    else:
                        frame = paint_chinese_opencv(
                            frame, citytxt, (303, yfir), fircolor, 12)
                    frame = paint_chinese_opencv(frame, str(
                        city[list(city.keys())[0]][0]), (378, y), (255, 0, 0), 12)
                    frame = paint_chinese_opencv(frame, str(
                        city[list(city.keys())[0]][1]), (423, y), (0, 0, 0), 12)
                    frame = paint_chinese_opencv(
                        frame, addtxt, (468, y), (255, 0, 0), 12)
                    frame = paint_chinese_opencv(frame, str(
                        city[list(city.keys())[0]][3]), (513, y), (0, 0, 0), 12)
                    frame = paint_chinese_opencv(frame, str(
                        city[list(city.keys())[0]][4]), (558, y), (0, 0, 0), 12)
            cv2.rectangle(frame, (35, 348), (35, 348), (0, 0, 0), 50)
            frame = paint_chinese_opencv(
                frame, "刷新", (16, 338), (255, 255, 255), 20)

            # TODO:事件响应
            def mousecallback(event, x, y, *args):
                global point, evt, down
                if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN or event == cv2.EVENT_MBUTTONDOWN:
                    evt = 2
                    down = True
                elif down and event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP or event == cv2.EVENT_MBUTTONUP:
                    point = [x, y]
                    evt = 1
                    down = False
                elif event == cv2.EVENT_MOUSEMOVE:
                    point = [x, y]
                    evt = 0

            cv2.setMouseCallback('COVID-19 Map of China', mousecallback)

            # TODO:显示屏幕
            cv2.namedWindow('COVID-19 Map of China', 0)
            cv2.imshow('COVID-19 Map of China', frame)
            cv2.setWindowTitle('COVID-19 Map of China', cap)

            # TODO:处理事件
            poses = POS.copy()
            # 香港澳门点击字体也算选择，因为太小了。
            # 这里复制一份字典，使用自己的函数添加字体对应的点吗，POS用于绘制不变。
            if 10 <= point[0] <= 60 and 323 <= point[1] <= 373 and evt == 1:
                print_info("Loading COVID-19 datas. ")
                print_info("Loading COVID-19 datas. ")
                importlib.reload(covids)
                from covids import (ADD_SORT, AREAS_SORT, CHINA_DEAD, CHINA_HEAL,
                                    CHINA_IMPORT, CHINA_LOCAL, CHINA_NO_INFECT,
                                    CHINA_NOW_CONFIRM, CHINA_SEVERE, CHINA_SUSPECT,
                                    CHINA_TOTAL, CITIES, NOW_SORT, CONFIRM_SORT,
                                    DEAD_SORT, GRADES, HEAL_SORT, LOCAL_SORT, TIME,
                                    NOT_UPDATE_PROVINCE, NOT_UPDATE_CITIES)
                print_info("Done. ")
            if not cities_view and point[0] in range(70, 130) and point[1] in range(323, 373) and evt == 1:
                showmode = 0
            if not cities_view and point[0] in range(130, 190) and point[1] in range(323, 373) and evt == 1:
                showmode = 1
            if not cities_view and point[0] in range(190, 250) and point[1] in range(323, 373) and evt == 1:
                showmode = 2
            if cities_view and 70 <= point[0] <= 120 and 323 <= point[1] <= 373 and evt == 1:
                cities_view = False
                page = 1
                pos = [0, 0]
                evt = 3
                continue
            if cities_view and point[0] in range(315, 376) and point[1] in range(315, 376) and evt == 1:
                if page - 1 > 0:
                    page -= 1
            if cities_view and point[0] in range(515, 576) and point[1] in range(315, 376) and evt == 1:
                if page + 1 <= int(len(CITIES[select]) / 5) + int(bool(len(CITIES[select]) % 5 / 1)):
                    page += 1
            legendflag = False
            for level in range(1, 8, 1):
                xrange = range(1, 9, 1)
                yrange = range(level * 20 - 20, level * 20 + 1)
                if point[0] in xrange and point[1] in yrange:
                    if evt == 1:
                        hides[level] = not hides[level]
                        legendflag = True
                    else:
                        highlights[level] = True
                        legendflag = True
                else:
                    highlights[level] = False
            for x in range(20):
                for y in range(10):
                    for place in SPEC_STATIC:
                        pos = TEXTS_POS[place]
                        poses[place] = spec_append(
                            poses[place], [pos[0] + x, pos[1] + y])
            flag = False
            for index, area in enumerate(poses):
                points = poses[area]
                mousepos = point
                if mousepos in points:
                    if not select_asked:
                        select = area
                    if not select_asked and evt == 1:
                        select = area
                        select_asked = True
                    if select_asked and evt == 1:
                        if not cities_view:
                            select = area
                    if select_asked and evt == 0:
                        if not cities_view:
                            select_asked_select = area
                    flag = True
            if not flag:
                if not select_asked:
                    select = ""
                if select_asked and evt == 1:
                    if point[0] in range(480, 580) and point[1] in range(290, 330) and evt == 1 and not cities_view:
                        cities_view = True
                        page = 1
                    elif cities_view:
                        pass
                    else:
                        select_asked_select = ""
                        select_asked = False
                        continue
                if select_asked and evt == 0:
                    if not cities_view:
                        select_asked_select = ""

            # TODO:更新
            k = cv2.waitKey(1)
            if not cv2.getWindowProperty('COVID-19 Map of China', cv2.WND_PROP_VISIBLE):
                break
            if k in [27, 81, 113]:
                break

        # TODO:结束销毁
        cv2.destroyAllWindows()
        print_info("End. ")
        sys.exit()
    except Exception as e:
        prtstr = str(int(round(float(perf_counter() - START), 4)
                     * 10000)) + " ERRS: " + str(e)
        print(prtstr)
        sys.exit()
else:
    del START

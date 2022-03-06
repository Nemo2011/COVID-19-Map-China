import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from covids import CHINA_TOTAL, CHINA_HEAL, CHINA_DEAD, CONFIRM_SORT, HEAL_SORT, DEAD_SORT, CITIES, AREAS
from posits import COLORS, POS

def paint_chinese_opencv(im, chinese, pos, color, size):
    img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    local = "simsun.ttc"
    font = ImageFont.truetype(local, size, encoding="utf-8")
    fillColor = color
    position = pos
    if not isinstance(chinese, str):
        chinese = chinese.decode('utf-8')
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, chinese, font=font, fill=tuple(fillColor))
    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow('COVID-19 Map of China', 0)
    cv2.resizeWindow('COVID-19 Map of China', 600, 383)
    select = ""
    point = [0, 0]
    evt = 0
    select_asked = False
    cities_view = False
    page = 1
    while True:
        def mousecallback(event, x, y, *args):
            global point, evt
            if event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONDOWN:
                point = [x, y]
                evt = 1
            elif event == cv2.EVENT_MOUSEMOVE:
                point = [x, y]
                evt = 0
        flag = False
        for index, area in enumerate(POS):
            points = POS[area]
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
                flag = True
        if not flag:
            if not select_asked:
                select = ""
            if select_asked and evt == 1:
                if point[0] in range(440, 591) and point[1] in range(235, 275) and evt == 1:
                    cities_view = True
                    page = 1
                elif cities_view:
                    pass
                else:
                    select_asked = False
        if point[0] >= 10 and point[0] <= 60 and point[1] >= 323 and point[1] <= 373 and evt == 1:
            break
        if cities_view and point[0] >= 70 and point[0] <= 120 and point[1] >= 323 and point[1] <= 373 and evt == 1:
            cities_view = False
            page = 1
        frame = cv2.imread("map_background.png")
        if not cities_view:
            if not select_asked:
                state_string = f"----中国----\n确诊{CHINA_TOTAL}人,\n治愈{CHINA_HEAL}人,\n死亡{CHINA_DEAD}人"
                frame = paint_chinese_opencv(frame, state_string, (445, 130), (0, 0, 0), 20)
                cv2.rectangle(frame, (440, 240), (590, 280), (0, 0, 0), 2)
                frame = paint_chinese_opencv(frame, "已选择：" + select, (445, 250), (0, 0, 0), 20)
            else:
                state_string = f"----{select}----\n确诊{CONFIRM_SORT[AREAS.index(select)]}人,\n治愈{HEAL_SORT[AREAS.index(select)]}人,\n死亡{DEAD_SORT[AREAS.index(select)]}人"
                frame = paint_chinese_opencv(frame, state_string, (445, 130), (0, 0, 0), 20)
                area = select
                cv2.rectangle(frame, (440, 235), (590, 275), [COLORS[area][2], COLORS[area][1], COLORS[area][0]], 2)
                frame = paint_chinese_opencv(frame, "   详细信息", (445, 245),(0, 0, 0), 20)
        else:
            cv2.rectangle(frame, (0, 0), (600, 383), (255, 255, 255), thickness=600)
            cv2.rectangle(frame, (95, 348), (95, 348), (0, 0, 0), 50)
            frame = paint_chinese_opencv(frame, "返回", (76, 338), (255, 255, 255), 20)
            area = select
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
                positions[index] = [positions[index][0] - leftmove, positions[index][1] - upmove]
        cv2.rectangle(frame, (35, 348), (35, 348), (0, 0, 0), 50)
        frame = paint_chinese_opencv(frame, "退出", (16, 338), (255, 255, 255), 20)
        if not cities_view:
            for idx, area in enumerate(POS):
                for pos in POS[area]:
                    if not select == area:
                        cv2.rectangle(frame, pos, pos, [COLORS[area][2], COLORS[area][1], COLORS[area][0]], thickness=1)
                    else:
                        cv2.rectangle(frame, pos, pos, [125, 125, 125], thickness=1)
        else:
            frame = paint_chinese_opencv(frame, select, (265, 0), COLORS[select], 30)
            for pos in positions:
                xbig = int(235 / pweight)
                ybig = int(318 / ptall)
                final = min(xbig, ybig)
                if final > 10:
                    final = 10
                newpos = [pos[0] * final, pos[1] * final]
                newweight = pweight * final + final * 2
                newtall = ptall * final + final * 2
                nxobjpos = (300 - newweight - final * 2) / 2
                nyobjpos = (383 - newtall - final * 2) / 2
                needminusx = xobjpos * final - nxobjpos
                needminusy = yobjpos * final - nyobjpos
                newpos = [newpos[0] - needminusx, newpos[1] - needminusy]
                newpos = [int(newpos[0]), int(newpos[1])]
                cv2.rectangle(frame, newpos, newpos, [COLORS[area][2], COLORS[area][1], COLORS[area][0]], final * 2)
        cv2.setMouseCallback('COVID-19 Map of China', mousecallback)
        cv2.namedWindow('COVID-19 Map of China', 0)
        cv2.imshow('COVID-19 Map of China', frame)
        k = cv2.waitKey(1)
        if not cv2.getWindowProperty('COVID-19 Map of China', cv2.WND_PROP_VISIBLE):
            break
        if k in [27, 81, 113]:
            break
    cv2.destroyAllWindows()

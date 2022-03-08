""" The main program of the map. """
import cv2
from datas import *
from tools import paint_chinese_opencv

if __name__ == '__main__':
    print("Staring...")
    #TODO:初始化
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow('COVID-19 Map of China', 0)
    cv2.resizeWindow('COVID-19 Map of China', 600, 383)
    select = ""
    point = [0, 0]
    evt = 0
    select_asked = False
    select_asked_select = ""
    cities_view = False
    page = 1

    while True:
        #TODO:处理事件
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
                if select_asked and evt == 0:
                    if not cities_view:
                        select_asked_select = area
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
                    select_asked_select = ""
                    select_asked = False
            if select_asked and evt == 0:
                if not cities_view:
                    select_asked_select = ""
        if point[0] >= 10 and point[0] <= 60 and point[1] >= 323 and point[1] <= 373 and evt == 1:
            break
        if cities_view and point[0] >= 70 and point[0] <= 120 and point[1] >= 323 and point[1] <= 373 and evt == 1:
            cities_view = False
            page = 1
        if cities_view and point[0] in range(300, 401) and point[1] in range(300, 401) and evt == 1:
            if page - 1 > 0:
                page -= 1
        if cities_view and point[0] in range(500, 600) and point[1] in range(300, 401) and evt == 1:
            if page + 1 <= int(len(CITIES[select]) / 5) + int(bool(len(CITIES[select]) % 5 / 1)):
                page += 1

        #TODO:绘制显示内容
        frame = cv2.imread("map_background.png")
        if not cities_view:
            if not select_asked:
                state_string = f"----中国----\n确诊{CHINA_TOTAL}人,\n死亡{CHINA_DEAD}人\n治愈{CHINA_HEAL}人"
                frame = paint_chinese_opencv(frame, state_string, (445, 130), (0, 0, 0), 20)
                cv2.rectangle(frame, (440, 240), (590, 280), (0, 0, 0), 2)
                frame = paint_chinese_opencv(frame, "已选择：" + select, (445, 250), (0, 0, 0), 20)
            else:
                state_string = f"----{select}----\n确诊{CONFIRM_SORT[AREAS.index(select)]}人,\n死亡{DEAD_SORT[AREAS.index(select)]}人,\n治愈{HEAL_SORT[AREAS.index(select)]}人"
                frame = paint_chinese_opencv(frame, state_string, (445, 130), (0, 0, 0), 20)
                area = select
                cv2.rectangle(frame, (440, 235), (590, 275), [COLORS[area][2], COLORS[area][1], COLORS[area][0]], 2)
                frame = paint_chinese_opencv(frame, "   详细信息", (445, 245),(0, 0, 0), 20)
            frame = paint_chinese_opencv(frame, "Update at: " + TIME, (0, 0), (0, 0, 0), 20)
            for idx, area in enumerate(POS):
                for pos in POS[area]:
                    if not select == area:
                        cv2.rectangle(frame, pos, pos, [COLORS[area][2], COLORS[area][1], COLORS[area][0]], thickness=1)
                    else:
                        cv2.rectangle(frame, pos, pos, [125, 125, 125], thickness=1)
                    if select_asked and select_asked_select == area:
                        cv2.rectangle(frame, pos, pos, [125, 125, 125], thickness=1)
        else:
            cv2.rectangle(frame, (0, 0), (600, 383), (255, 255, 255), thickness=600)
            cv2.rectangle(frame, (95, 348), (95, 348), (0, 0, 0), 50)
            cv2.line(frame, (0, 40), (600, 40), (0, 0, 0), 5)
            cv2.line(frame, (300, 40), (300, 383), (0, 0, 0), 5)
            cv2.line(frame, (300, 100), (600, 100), (0, 0, 0), 5)
            if len(CITIES[select]) - page * 5 >= 0:
                cityrange = list(range(0, len(CITIES[select])))[(page - 1) * 5:page * 5]
            else:
                cityrange = list(range(0, len(CITIES[select])))[(page - 1) * 5:len(CITIES[select])]
            select_lst = TOTALS[select]
            citylst = [{f"{select}所有":select_lst}]
            for index, key in enumerate(CITIES[select]):
                if index in cityrange:
                    citylst.append({key:CITIES[select][key]})
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
            frame = paint_chinese_opencv(frame, select, (265, 0), (0, 0, 0), 30)
            for pos in positions:
                xbig = int(280 / pweight)
                ybig = int(200 / ptall)
                final = min(xbig, ybig)
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
                cv2.rectangle(frame, newpos, newpos, [COLORS[area][2], COLORS[area][1], COLORS[area][0]], int(final * 2))
            cv2.line(frame, (300, 40), (300, 285), (0, 0, 0), 5)
            cv2.line(frame, (420, 40), (420, 285), (0, 0, 0), 5)
            cv2.line(frame, (480, 40), (480, 285), (0, 0, 0), 5)
            cv2.line(frame, (540, 40), (540, 285), (0, 0, 0), 5)
            cv2.line(frame, (300, 285), (600, 285), (0, 0, 0), 5)
            frame = paint_chinese_opencv(frame, "城市", (305, 45), (0, 0, 0), 20)
            frame = paint_chinese_opencv(frame, "确诊", (425, 45), (0, 0, 0), 20)
            frame = paint_chinese_opencv(frame, "死亡", (485, 45), (0, 0, 0), 20)
            frame = paint_chinese_opencv(frame, "治愈", (545, 45), (0, 0, 0), 20)
            cv2.line(frame, (300, 75), (600, 75), (0, 0, 0), 5)
            cv2.rectangle(frame, (350, 335), (350, 335), (125, 125, 125), 50)
            cv2.rectangle(frame, (550, 335), (550, 335), (125, 125, 125), 50)
            frame = paint_chinese_opencv(frame, f"{page}/{int(len(CITIES[select]) / 5) + int(bool(len(CITIES[select]) % 5 / 1))}", (440, 326), (0, 0, 0), 20)
            frame = paint_chinese_opencv(frame, "<-", (340, 326), (0, 0, 0), 20)
            frame = paint_chinese_opencv(frame, "->", (540, 326), (0, 0, 0), 20)
            for index, city in enumerate(citylst):
                y = 75 + 35 * index + 5
                frame = paint_chinese_opencv(frame, list(city.keys())[0], (305, y), (0, 0, 0), 15)
                frame = paint_chinese_opencv(frame, str(city[list(city.keys())[0]][0]), (425, y), (0, 0, 0), 15)
                frame = paint_chinese_opencv(frame, str(city[list(city.keys())[0]][1]), (485, y), (0, 0, 0), 15)
                frame = paint_chinese_opencv(frame, str(city[list(city.keys())[0]][2]), (545, y), (0, 0, 0), 15)
        cv2.rectangle(frame, (35, 348), (35, 348), (0, 0, 0), 50)
        frame = paint_chinese_opencv(frame, "退出", (16, 338), (255, 255, 255), 20)

        #TODO:事件响应
        def mousecallback(event, x, y, *args):
            global point, evt
            if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN or event == cv2.EVENT_MBUTTONDOWN:
                point = [x, y]
                evt = 1
            elif event == cv2.EVENT_MOUSEMOVE:
                point = [x, y]
                evt = 0
        cv2.setMouseCallback('COVID-19 Map of China', mousecallback)

        #TODO:显示屏幕
        cv2.namedWindow('COVID-19 Map of China', 0)
        cv2.imshow('COVID-19 Map of China', frame)
        cv2.setWindowTitle('COVID-19 Map of China', 'COVID-19 Map of China')

        #TODO:更新
        pos = [0, 0]
        evt = 0
        k = cv2.waitKey(1)
        if not cv2.getWindowProperty('COVID-19 Map of China', cv2.WND_PROP_VISIBLE):
            break
        if k in [27, 81, 113]:
            break

    #TODO:结束销毁
    cv2.destroyAllWindows()
    print("End.")

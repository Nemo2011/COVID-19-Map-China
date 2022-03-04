import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from covids import CHINA_TOTAL, CHINA_HEAL, CHINA_DEAD, CONFIRM_SORT, HEAL_SORT, DEAD_SORT
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
    draw.text(position, chinese, font=font, fill=fillColor)
    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow('COVID-19 Map of China', 0)
    cv2.resizeWindow('COVID-19 Map of China', 600, 383)
    select = ""
    point = [0, 0]
    evt = 0
    while True:
        def mousecallback(event, x, y, flags, param):
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
                select = area
                flag = True
        if not flag:
            select = ""
        if point[0] >= 10 and point[0] <= 60 and point[1] >= 323 and point[1] <= 373 and evt == 1:
            break
        frame = cv2.imread("map_background.png")
        for idx, area in enumerate(POS):
            for pos in POS[area]:
                if not select == area:
                    cv2.rectangle(frame, pos, pos, [COLORS[area][2], COLORS[area][1], COLORS[area][0]], thickness=1)
                else:
                    cv2.rectangle(frame, pos, pos, [125, 125, 125], thickness=1)
        cv2.rectangle(frame, (35, 348), (35, 348), (0, 0, 0), 50)
        frame = paint_chinese_opencv(frame, "退出", (16, 338), (255, 255, 255), 20)
        cv2.rectangle(frame, (440, 190), (590, 225), (0, 0, 0), 2)
        state_string = f"中国：\n确诊{CHINA_TOTAL}人"
        frame = paint_chinese_opencv(frame, state_string, (445, 130), (0, 0, 0), 20)
        frame = paint_chinese_opencv(frame, "已选择：" + select, (445, 200), (0, 0, 0), 20)
        cv2.setMouseCallback('COVID-19 Map of China', mousecallback)
        cv2.namedWindow('COVID-19 Map of China', 0)
        cv2.imshow('COVID-19 Map of China', frame)
        k = cv2.waitKey(1)
        if not cv2.getWindowProperty('COVID-19 Map of China', cv2.WND_PROP_VISIBLE):
            break
        if k in [27, 81, 113]:
            break
    cv2.destroyAllWindows()

import time
import cv2
import numpy

COLORS = {
	"湖北":(133, 133, 208),  
	"湖南":(0, 168, 243),  
	"河北":(255, 210, 225),  
	"河南":(203, 124, 124),  
	"广西":(190, 33, 15),  
	"广东":(0, 0, 0),  
	"内蒙古":(14, 209, 69),  
	"新疆":(255, 242, 0),  
	"西藏":(184, 61, 186),  
	"宁夏":(136, 0, 27),  
	"福建":(129, 156, 173),  
	"吉林":(162, 82, 157),  
	"安徽":(211, 200, 248),  
	"浙江":(151, 209, 246),  
	"云南":(216, 227, 228),  
	"贵州":(255, 202, 24),  
	"辽宁":(116, 91, 118),  
	"黑龙江":(241, 114, 250),  
	"四川":(97, 109, 169),  
	"青海":(140, 255, 251), 
	"甘肃":(255, 127, 39),
	"山西":(220, 186, 186),  
	"陕西":(88, 88, 88),  
	"山东":(1, 171, 157),  
	"海南":(63, 72, 204),  
	"台湾":(196, 255, 14),  
	"香港":(255, 174, 200),  
	"澳门":(90, 49, 127),  
	"江苏":(133, 246, 186),  
	"北京":(236, 28, 36),  
	"天津":(177, 162, 92), 
	"上海":(192, 153, 94),  
	"重庆":(82, 39, 34),
	"江西":(252, 121, 121)
}

POS = {
    "湖北":[],
    "湖南":[], 
    "河北":[],  
    "河南":[],
    "广西":[],
    "广东":[], 
    "内蒙古":[],
    "新疆":[],
    "西藏":[], 
    "宁夏":[],
    "福建":[],
    "吉林":[],
    "安徽":[],
    "浙江":[],
    "云南":[],
    "贵州":[],
    "辽宁":[],
    "黑龙江":[],
    "四川":[],
    "青海":[],
    "甘肃":[],
    "山西":[],  
    "陕西":[],
    "山东":[],  
    "海南":[], 
    "台湾":[],
    "香港":[],
    "澳门":[],
    "江苏":[],
    "北京":[],
    "天津":[], 
    "上海":[], 
    "重庆":[],
    "江西":[],
}

print("Loading Map Datas...")
start = time.perf_counter()
pic = cv2.imread("map_colored.png")
array = numpy.array(pic)
for row in range(383):
    for col in range(600):
        clr = array[row][col]
        new_clr = [clr[2], clr[1], clr[0]]
        for idx, area in enumerate(COLORS):
            area_clr = COLORS[area]
            area_clr = list(area_clr)
            new_clr = list(new_clr)
            if area_clr == new_clr:
                POS[area].append([col, row])
end = time.perf_counter()
print(f"Done in {round(end - start, 3)} seconds. ")

if __name__ == '__main__':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow('frame', 0)
    cv2.resizeWindow('frame', 600, 383)
    while True:
        frame = cv2.imread("map_background.png")
        for idx, area in enumerate(POS):
            for pos in POS[area]:
                cv2.rectangle(frame, pos, pos, [COLORS[area][2], COLORS[area][1], COLORS[area][0]], thickness=1)
        cv2.namedWindow('frame', 0)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        if not cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE):
            break
        if k in [27, 81, 113]:
            break
    cv2.destroyAllWindows()

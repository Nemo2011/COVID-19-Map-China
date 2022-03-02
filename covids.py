import json
import sys
import time
import requests

print("Loading COVID-19 datas...")
start = time.perf_counter()
try:
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
    r = requests.get(url=url)
    data = json.loads(r.json()['data'])
    json.dump(data, open("covids.json", "w"), indent=4)
except:
    print("Loading datas error. Please check your Internet. ")
    sys.exit()
total_lst = []
total_dead = []
total_dict = {}
areas = []
last_time = ""
last_time = data['lastUpdateTime']
for area in data['areaTree'][0]['children']:
    area_name = area['name']
    area_confirm = area['total']['confirm']
    area_dead = area['total']['dead']
    area_heal = area['total']['heal']
    total_lst.append(area_confirm)
    total_dead.append(area_dead)
    total_dict[area_name] = [area_confirm, area_dead, area_heal]
def get_key(obj, dct):
    for key in dct:
        if dct[key][0] == obj:
            return key
new_dead = []
new_heal = []
total_lst.sort()
for num in total_lst:
    areas.append(get_key(num, total_dict))
    new_dead.append(total_dict[get_key(num, total_dict)][1])
    new_heal.append(total_dict[get_key(num, total_dict)][2])
total_lst = total_lst[::-1]
new_dead = new_dead[::-1]
new_heal = new_heal[::-1]
areas = areas[::-1]
end = time.perf_counter()
print(f"Done in {round(end - start, 3)} seconds. ")

if __name__ == '__main__':
    from plotly import offline
    from plotly.graph_objs import Bar, Layout
    print("制作图表...")
    databar = Bar(x=areas, y=total_lst, name="存活人数", marker_color='rgb(0, 0, 255)')
    x_conf = {"title":"地区"}
    y_conf = {"title":"确诊病例"}
    layout = Layout(title=f"中国各省、自治区、直辖市的新冠病毒确诊病例({last_time}更新)", xaxis=x_conf, yaxis=y_conf, barmode="stack")
    offline.plot({'data':databar, 'layout':layout}, filename="Confirm-Datas-Tests.html", show_link=True)
else:
    CHINA_TOTAL = data['chinaTotal']['confirm']
    CHINA_DEAD = data['chinaTotal']['dead']
    CHINA_HEAL = data['chinaTotal']['heal']
    AREAS_SORT = areas
    CONFIRM_SORT = total_lst
    DEAD_SORT = new_dead
    HEAL_SORT = new_heal

""" COVID-19's data's sets. """
import json
import sys
from time import sleep, time
import requests


def print_info(msg: str) -> None:
    """
        @brief Print informations. 
        This function is only use for covids.py(covids). 
        @param msg The message need to print. 
    """
    prtstr = "COVID-DATA: " + msg
    print(prtstr)


def print_errs(msg: str) -> None:
    """
        @brief Print errors. 
        This function is only use for covids.py(covids). 
        @param msg The message need to print. 
    """
    prtstr = "COVID-DATA: " + msg
    print(prtstr)


def get_key_lists_index(obj: object, dct: dict, idx: int = 0) -> object:
    """
        @brief Get the key in the total list dict. 
        The dict will like:{"a":list(), "b":list(), ...}
        @param obj The finding object. 
        @param dct The dict. 
        @param idx The index to look-up in the each list.
    """
    for key in dct:
        if dct[key][idx] == obj:
            return key


print("COVID-DATA: Loading ...")

# TODO:爬取数据
load = True
data = {}
while load:
    try:
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(
            time() * 1000)
        r = requests.get(url=url)
        data = json.loads(r.json()['data'])
        with open("covids.json", "w+") as file:
            json.dump(data, file, indent=4)
        load = False
    except Exception as e:
        print_errs(str(e))
        sleep(5)
        continue
    else:
        print_info("Gets the json data successfully. ")

# TODO:处理数据
try:
    total_lst = []
    total_dict = {}
    areas = []
    not_updates_province = []
    last_time = data['lastUpdateTime']
    for area in data['areaTree'][0]['children']:
        area_name = area['name']
        area_confirm = area['total']['confirm']
        area_dead = area['total']['dead']
        area_heal = area['total']['heal']
        area_add = area['today']['confirm']
        area_now = area['total']['nowConfirm']
        area_local = area['total']['provinceLocalConfirm']
        total_lst.append(area_confirm)
        total_dict[area_name] = [area_confirm, area_now,
                                 area_add, area_dead, area_heal, area_local]
        if area['today']['isUpdated'] == False:
            not_updates_province.append(area['name'])
    new_dead = []
    new_heal = []
    new_add = []
    new_local = []
    new_now = []
    total_lst.sort()
    for num in total_lst:
        areas.append(get_key_lists_index(num, total_dict))
        new_now.append(total_dict[get_key_lists_index(num, total_dict)][1])
        new_heal.append(total_dict[get_key_lists_index(num, total_dict)][4])
        new_dead.append(total_dict[get_key_lists_index(num, total_dict)][3])
        new_add.append(total_dict[get_key_lists_index(num, total_dict)][2])
        new_local.append(total_dict[get_key_lists_index(num, total_dict)][5])
    total_lst = total_lst[::-1]
    new_now = new_now[::-1]
    new_dead = new_dead[::-1]
    new_heal = new_heal[::-1]
    new_add = new_add[::-1]
    new_local = new_local[::-1]
    areas = areas[::-1]
    cities = {}
    total_grades = {}
    cities_not_update = {}
    for area in areas:
        cities_data = []
        for index, cs in enumerate(data['areaTree'][0]['children']):
            if cs['name'] == area:
                cities_data = (data['areaTree'][0]
                               ['children'][index]['children'])
        new_data = {}
        grades = {}
        not_update = []
        for city in cities_data:
            if 'grade' in list(city['total'].keys()):
                if city['total']['grade'] != "点击查看详情":
                    if city['name'].count("待确认") != 1:
                        if city['name'].count("境外") != 1 and city['name'].count("外地") != 1:
                            grades[city['name']] = city['total']['grade']
            if city['today']['isUpdated'] == False:
                not_update.append(city['name'])
            name = city['name']
            new_data[city['name']] = [city['total']['confirm'], city['total']['nowConfirm'],
                                      city['today']['confirm'], city['total']['dead'], city['total']['heal']]
        sort_data = {}
        for key in new_data:
            if key.count("待确认") >= 1:
                sort_data[key] = new_data[key]
            elif key == "境外输入":
                sort_data[key] = new_data[key]
            elif key.count("境外") == 1:
                sort_data[key] = new_data[key]
            elif key.count("外地") == 1:
                sort_data[key] = new_data[key]
        for key in new_data:
            if not key in sort_data.keys():
                sort_data[key] = new_data[key]
        cities[area] = sort_data
        total_grades[area] = grades
        cities_not_update[area] = not_update

    # TODO:整理数据
    TIME = data["lastUpdateTime"]
    CITIES = cities
    GRADES = total_grades
    CHINA_TOTAL = data['chinaTotal']['confirm'], data['chinaAdd']['confirm']
    CHINA_DEAD = data['chinaTotal']['dead'], data['chinaAdd']['dead']
    CHINA_HEAL = data['chinaTotal']['heal'], data['chinaAdd']['heal']
    CHINA_NOW_CONFIRM = data['chinaTotal']['nowConfirm'], data['chinaAdd']['nowConfirm']
    CHINA_SUSPECT = data['chinaTotal']['suspect'], data['chinaAdd']['suspect']
    CHINA_SEVERE = data['chinaTotal']['nowSevere'], data['chinaAdd']['nowSevere']
    CHINA_IMPORT = data['chinaTotal']['importedCase'], data['chinaAdd']['importedCase']
    CHINA_NO_INFECT = data['chinaTotal']['noInfect'], data['chinaAdd']['noInfect']
    CHINA_LOCAL = data['chinaTotal']['localConfirm'], data['chinaAdd']['localConfirm']
    AREAS_SORT = areas
    NOW_SORT = new_now
    CONFIRM_SORT = total_lst
    DEAD_SORT = new_dead
    HEAL_SORT = new_heal
    ADD_SORT = new_add
    LOCAL_SORT = new_local
    NOT_UPDATE_CITIES = cities_not_update
    NOT_UPDATE_PROVINCE = not_updates_province

    # TODO:结束
    print_info("Done. ")
except Exception as e:
    print_errs(str(e))
    sys.exit()
else:
    del [
        area,
        area_add,
        area_confirm,
        area_dead,
        area_heal,
        area_local,
        area_name,
        area_now,
        areas,
        cities,
        cities_data,
        city,
        cs,
        # data,
        file,
        grades,
        index,
        key,
        last_time,
        load,
        name,
        new_add,
        new_data,
        new_dead,
        new_heal,
        new_local,
        new_now,
        num,
        r,
        sort_data,
        total_dict,
        total_grades,
        total_lst,
        url
    ]

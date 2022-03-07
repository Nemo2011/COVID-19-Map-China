""" The useful functions the program need. """
# You can copy texts on this file out of the license. 
from typing import Any, Union
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont
#TODO:函数1：通过对象获取列表字典中一项的下表。
def get_key_lists_index(obj:Any, dct:dict, index:int=0):
    """
        Get the key in the total list dict. 
        @param:obj:The finding object. 
        @param:dct:The dict. 
        @param:index:The index to look-up in the each list. 
    """
    for key in dct:
        if dct[key][index] == obj:
            return key

#TODO:函数2：在OpenCV画布上绘制中文（不乱码）
def paint_chinese_opencv(im:Any, chinese:str, pos:Union[tuple, list], color:Union[tuple, list], size:Union[int, float]):
    """
        Drawing chinese on opencv drawing map. 
        Need simsun.ttc. 
        @param:im:Image in cv2. 
        @param:chinese:The text. 
        @param:pos:Position of x, y. 
        @param:color:BGR color of the text. 
        @param:size:The size of the text. 
    """
    img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    local = "simsun.ttc"
    font = ImageFont.truetype(local, size, encoding="utf-8")
    fillColor = color
    position = pos
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, chinese, font=font, fill=tuple(fillColor))
    img = cv2.cvtColor(numpy.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img

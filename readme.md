# 中国疫情地图 COVID-19-MAP-CHINA

版本0.3.1（预发布）

## Overview 预览

中国疫情一览地图。采用可视化设计，分为五个等级，一览感染人数、死亡人数等信息。

## Usage 用法

功能暂未完善。地图加载器和病毒数据加载器测试：直接运行。

## Changelog [更新记录](changelog.md)

## Third-Party 第三方库

安装：`pip install -r requirements.txt`
运行病毒数据加载器测试：附加`pip install -r requirements.add-ons.txt`

## Notice 注意

此项目的地图在原图上经过了特殊的处理。有的地方不是1：1或者不是非常得像，这些全是为了用户的使用体验，现指出所有经过修改的部分：

- 1. 香港经过了变大处理，因此看着和上海一样大。
- 2. 澳门也经过了变大处理，但是没有香港大，像素比为1:2。
- 3. 河北廊坊市北部地区（即为四周被北京和天津包围的部分，隶属廊坊市）原来导入的地图是没有的，后来经过了添加，可能与实际不太相符。
- 4. 原图地址为：[点击前往](https://gss0.baidu.com/-Po3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/962bd40735fae6cd1851ec8201b30f2443a70f6f.jpg)，涂色的图是原图经过了特殊处理的。

# -*- encoding:utf-8 -*-
"""
@文件        :getCities.py
@说明        :
@时间        :22/06/08/0008 19:52
@作者        :eleven
@软件        :PyCharm
"""


def getcities(file):
    lines = open(file)
    cities = []
    for line in lines:
        line = line.strip('\n')
        cities.append(line)
    return cities


if __name__ == '__main__':
    city = getcities('HotCities.txt')
    print(city)

# -*- encoding:utf-8 -*-
"""
@文件        :getDate.py
@说明        :
@时间        :22/06/08/0008 20:02
@作者        :eleven
@软件        :PyCharm
"""


def getdate():
    date = []
    years = []
    months = []
    for i in range(2014, 2023):
        years.append(i)
    for j in range(1, 13):
        months.append(j)
    for year in years[:-1]:
        for month in months:
            if month < 10:
                data = str(year) + "0" + str(month)
            else:
                data = str(year) + "" + str(month)
            date.append(data)
    for month in months[0:5]:
        date.append(str(2022) + "0" + str(month))
    return date


if __name__ == '__main__':
    date = getdate()
    print(date)

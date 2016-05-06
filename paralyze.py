# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

from model import Job
import datetime
import matplotlib.pyplot as plt

from util import chinese_to_pinyin


def main():
    python = Job.select().where(Job.position_name == 'python')
    java = Job.select().where(Job.position_name == 'java')
    php = Job.select().where(Job.position_name == 'php')
    c_plus = Job.select().where(Job.position_name == 'c++')
    c = Job.select().where(Job.position_name == 'c')

    positions = {
        'python': python,
        'java': java,
        'php': php,
        'c++': c_plus,
        'c': c
    }
    cities = ['北京', '上海', '广州', '深圳', '杭州']

    positionnum_city(positions, cities)


def positionnum_city(positions, cities):
    ys = {}
    for position in positions:
        y = []
        for city in cities:
            y.append(
                positions[position].where(Job.city == city).count()
            )
        ys[position] = y

    x = [i+1 for i in range(len(cities))]

    max_y = []
    for y in ys:
        plt.plot(x, ys[y], '.', linewidth=2, linestyle='-', label=y)
        max_y.append(max(ys[y]))
    plt.legend(loc='upper right')


    plt.axis([0, len(cities)+1, 0, max(max_y)+500])
    # plt.xticks((1,2,3,4,5))

    x_cities = ''
    for i in cities:
        x_cities += chinese_to_pinyin(i)+str('                    ')
    plt.xlabel(x_cities)
    # plt.xlabel('BeiJing    ShangHai    GuangZhou    ShenZhen    HangZhou')

    plt.ylabel('Position Num')

    plt.title('Position Num - City', fontsize=14, fontweight='bold')
    plt.grid(True)
    plt.show()





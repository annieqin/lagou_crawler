# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import re
from model import Job
import datetime
import matplotlib.pyplot as plt
import numpy as np

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
    # cities = ['北京']

    # positionnum_city(positions, cities)

    salary_city(positions, cities)


def salary_city(positions, cities):
    # salaries = {'python':
    #               {'北京': [15, 20, ...],
    #                '上海': [10, 15, ...],
    #                ...
    #               },
    #              ...
    #            }
    salaries = {}
    for position in positions:
        s_city = {}
        for city in cities:
            s_city[city] = []
            p = positions[position].where(Job.city == city)
            for i in p:
                re_salary = re.findall(r'\d{1,2}', i.salary)
                if re_salary:
                    if len(re_salary) == 2:
                        re_salary = (int(re_salary[0]) + int(re_salary[1])) / 2
                    else:
                        re_salary = int(re_salary[0])
                s_city[city].append(re_salary)
            s_city[city] = np.mean(np.array(s_city[city]))
        salaries[position] = s_city

    x = [i+1 for i in range(len(cities))]
    ys = {}
    for position in positions:
        y = []
        for city in cities:
            y.append(salaries[position][city])
        ys[position] = y

    max_y = []
    min_y = []
    for y in ys:
        plt.plot(x, ys[y], '.', linewidth=2, linestyle='-', label=y)
        max_y.append(max(ys[y]))
        min_y.append(min(ys[y]))
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.legend(loc='center left')
    plt.axis([0, len(cities)+1, min(min_y), max(max_y)])

    x_cities = ''
    for i in cities:
        x_cities += chinese_to_pinyin(i)+str('    ')
    plt.xlabel(x_cities)

    plt.ylabel('Salary (k)')

    plt.title('Salary - City', fontsize=14, fontweight='bold')
    plt.grid(True)
    plt.show()


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





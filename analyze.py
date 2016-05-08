# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import re
from collections import defaultdict
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

    positionnum_city(positions, cities)
    # salary_city(positions, cities)
    # companysize_city(positions, cities)
    # salary_workyear(positions)


def salary_workyear(positions):
    salaries = {}
    # work_year = set()
    for position in positions:
        salaries_position = defaultdict(list)
        p = positions[position].select(Job.work_year,
                                       Job.salary,
                                       Job.position_name)
        for i in p:
            re_salary = re.findall(r'\d{1,2}', i.salary)
            if re_salary:
                if len(re_salary) == 2:
                    re_salary = (int(re_salary[0]) + int(re_salary[1])) / 2
                else:
                    re_salary = int(re_salary[0])
            re_workyear = re.search(r'\d{1,2}-\d{1,2}|\d{1,2}', i.work_year)
            if re_workyear:
                salaries_position[re_workyear.group()].append(re_salary)
                # work_year.add(re_workyear.group())
            else:
                salaries_position[i.work_year].append(re_salary)
                # work_year.add(i.work_year)
        salaries[position] = salaries_position
    work_year = [u'\u4e0d\u9650', u'\u5e94\u5c4a\u6bd5\u4e1a\u751f', '1', '1-3', '3-5', '5-10']

    for p in salaries:
        for wy in salaries[p]:
            salaries[p][wy] = np.mean(np.array(salaries[p][wy]))

    x = [i+1 for i in range(len(work_year))]

    ys = {}
    for p in salaries:
        y = []
        for w in work_year:
            if salaries[p][w]:
                y.append(salaries[p][w])
            else:
                y.append(0)
        ys[p] = y

    xticks = ('NoLimit', 'Graduates', '<1', '1-3', '3-5', '5-10')

    draw(x, ys, 2, 2, xticks, 'Work Year', 'Salary (k)', 'Work Year - Salary')


def companysize_city(positions, cities):
    companysize = {}
    for position in positions:
        c_city = {}
        for city in cities:
            c_city[city] = []
            c = positions[position].where(Job.city == city)
            for i in c:
                re_size = re.findall(r'\d{1,5}', i.company_size)
                if re_size:
                    if len(re_size) == 2:
                        re_size = (int(re_size[0]) + int(re_size[1])) / 2
                    else:
                        re_size = int(re_size[0])
                c_city[city].append(re_size)
            c_city[city] = np.mean(np.array(c_city[city]))
        companysize[position] = c_city

    x = [i+1 for i in range(len(cities))]
    ys = {}
    for position in positions:
        y = []
        for city in cities:
            y.append(companysize[position][city])
        ys[position] = y

    xticks = ('BeiJing', 'ShangHai', 'GuangZhou', 'ShenZhen', 'HangZhou')

    draw(x, ys, 100, 100, xticks, 'City', 'Company Size', 'City - Company Size')


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

    xticks = ('BeiJing', 'ShangHai', 'GuangZhou', 'ShenZhen', 'HangZhou')

    draw(x, ys, 1, 1, xticks, 'City', 'Salary (k)', 'City - Salary')


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

    xticks = ('BeiJing', 'ShangHai', 'GuangZhou', 'ShenZhen', 'HangZhou')

    # draw(x, ys, 500, 500, xticks, 'City',
    #      'Position Num', 'City - Position Num')
    draw_bar(x, ys, xticks, 'City',  'Position Num', 'City - Position Num')


def draw(x, ys, ybottom, ytop, xticks, xlabel, ylabel, title):
    max_y = []
    min_y = []
    for y in ys:
        plt.plot(x, ys[y], '.', linewidth=2, linestyle='-', label=y)
        max_y.append(max(ys[y]))
        min_y.append(min(ys[y]))

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.legend(loc='best')
    plt.axis([0, len(x)+1, min(min_y)-ybottom, max(max_y)+ytop])

    index = np.arange(len(x))
    offset = 1
    plt.xticks(index+offset, xticks)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title(title, fontsize=14, fontweight='bold')

    plt.grid(True)
    plt.show()


def draw_bar(x, ys, xticks, xlabel, ylabel, title):
    index = np.arange(len(x))
    # index = [i+1 for i in range(len(x))]
    bar_width = 0.18
    offset = 0
    opacity = 0.4
    for y in ys:
        plt.bar(index+offset, ys[y], bar_width,
                label=y, color=np.random.rand(3, 1), alpha=opacity,)
        offset += 0.18
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index+(offset/2), xticks)
    plt.legend()
    plt.show()
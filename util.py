# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'


def chinese_to_pinyin(word):
    words = {
        '北京': 'BeiJing',
        '上海': 'ShangHai',
        '广州': 'GuangZhou',
        '深圳': 'ShenZhen',
        '杭州': 'HangZhou'
    }

    return words[word]
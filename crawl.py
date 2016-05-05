# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import requests
from peewee import *

mysql_db = MySQLDatabase('lagou', host='127.0.0.1', port=3306, user='root')


class BaseModel(Model):
    class Meta:
        database = mysql_db


def create_tables():
    mysql_db.connect()
    mysql_db.create_tables([Job], safe=True)


class Job(BaseModel):
    position_id = CharField(max_length=50, default='')
    city = CharField(max_length=100, default='')
    company_name = CharField(max_length=100, default='')
    company_short_name = CharField(max_length=1000, default='')
    company_size = CharField(max_length=100, default='')

    create_time = CharField(max_length=500, default='')

    education = CharField(max_length=100, default='')

    finance_stage = CharField(max_length=100, default='')

    industry_field = CharField(max_length=100, default='')

    position_name = CharField(max_length=100, default='')
    position_first_type = CharField(max_length=100, default='')
    position_type = CharField(max_length=100, default='')

    job_nature = CharField(max_length=25, default='')

    salary = CharField(max_length=100, default='')
    work_year = CharField(max_length=100, default='')


def requests_post(url, params=None, payload=None):
    res = requests.post(url,
                        params=params,
                        data=payload)
    return res


def main():
    cities = ['北京', '上海', '广州', '深圳', '杭州']
    positions = ['python', 'java', 'php', 'c', 'c++', 'ruby',
                 '.net', 'c#', 'node.js', 'go']

    payload = {
        'first': False,
        'pn': 1,
        'kd': ''
    }
    params = {
        'city': ''
    }

    for p in positions:
        payload['kd'] = p
        for c in cities:
            pn = 1
            flag = True
            params['city'] = c
            while flag:
                payload['pn'] = pn
                print 'Crawling '+p+' '+c+' '+str(pn)
                response = requests_post('http://www.lagou.com/jobs/positionAjax.json',
                                         params=params,
                                         payload=payload)
                result = response.json()['content']['result']

                if result:
                    try:
                        with mysql_db.atomic():
                            for res in result:
                                job = Job.select().where(Job.position_id == res['positionId']).exists()
                                if not job:
                                    item = {}
                                    item['position_id'] = res['positionId']
                                    item['city'] = params['city']
                                    item['company_name'] = res['companyName']
                                    item['company_short_name'] = res['companyShortName']
                                    item['company_size'] = res['companySize']
                                    item['create_time'] = res['createTime']
                                    item['education'] = res['education']
                                    item['finance_stage'] = res['financeStage']
                                    item['industry_field'] = res['industryField']
                                    item['position_name'] = payload['kd']
                                    item['position_first_type'] = res['positionFirstType']
                                    item['position_type'] = res['positionType']
                                    item['job_nature'] = res['jobNature']
                                    item['salary'] = res['salary']
                                    item['work_year'] = res['workYear']

                                    Job.create(**item)
                    except:
                        print 'mysql insert exception'

                    pn += 1

                else:
                    flag = False
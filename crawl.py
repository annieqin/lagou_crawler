# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

import requests
from peewee import *
import multiprocessing
import os
from datetime import datetime

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


def crawling(task):
    payload = {
        'first': False,
        'kd': task[0],
        'pn': task[2],
    }
    params = {
        'city': task[1]
    }

    print str(os.getpid())+' Crawling '+task[0]+' '+task[1]+' '+str(task[2])
    response = requests_post(
        'http://www.lagou.com/jobs/positionAjax.json',
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
            print str(os.getpid())+' mysql insert exception'
        for i in range(1, 5):

            queue.put((task[0], task[1], task[2]+i))
        return
    else:
        return


def working(ns, queue, rlock):
    while True:
        if rlock.acquire():
            if not queue.empty():
                task = queue.get()
                visited_pages = ns.visited_pages
                if task in visited_pages:
                    queue.task_done()
                    rlock.release()
                    continue
                visited_pages.add(task)
                ns.visited_pages = visited_pages
                rlock.release()

                crawling(task)
                continue
            else:
                rlock.release()
                break


manager = multiprocessing.Manager()
ns = manager.Namespace()
ns.visited_pages = set()
queue = manager.Queue()
rlock = manager.RLock()


def main():
    cities = ['北京', '上海', '广州', '深圳']
    positions = ['python', 'java', 'php', 'c', 'c++',
                 'ruby', '.net', 'c#', 'node.js', 'go']

    for p in positions:
        for c in cities:
            queue.put((p, c, 1))
    start_time = datetime.now()
    processes = []
    for i in range(4):
        process = multiprocessing.Process(
            target=working, args=(ns, queue, rlock)
        )
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    end_time = datetime.now()
    print '多进程用时 '+str(end_time-start_time)

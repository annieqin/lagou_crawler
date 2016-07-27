# coding: utf-8

__author__ = 'qinanlan <qinanlan@domob.com>'

import gevent
from gevent import monkey

from gevent.queue import Queue
import requests

from datetime import datetime


class Crawl(object):
    def __init__(self,
                 cities=('北京', '上海', '广州', '深圳', '杭州'),
                 positions=('python', 'java', 'php', 'c', 'c++')):
        monkey.patch_socket()

        self.task_queue = Queue()
        self.visited_pages = []
        self.is_continue = True

        for p in positions:
            for c in cities:
                self.task_queue.put((p, c, 1))

    def crawling(self, w):
        while not self.task_queue.empty():
            task = self.task_queue.get()

            if task in self.visited_pages:
                print '退出！'
                break
            self.visited_pages.append(task)
            print 'Crawling '+'  '+str(id(gevent.Greenlet.getcurrent()))+str(task[0])+str(task[1])+str(task[2])

            payload = {
                'first': False,
                'kd': task[0],
                'pn': task[2],
            }
            params = {
                'city': task[1]
            }
            # gevent.sleep(0)
            response = requests.post(
                'http://www.lagou.com/jobs/positionAjax.json',
                params=params,
                data=payload).json()

            result = response.get('content')

            if result:
                w.send(task)

            else:
                self.is_continue = False

    def working(self):
        print 'Working '+'  '+str(id(gevent.Greenlet.getcurrent()))
        while self.is_continue:
            task = yield
            for i in range(1, 5):
                self.task_queue.put((task[0], task[1], task[2]+i))

    def run(self):
        start_time = datetime.now()
        gevent_threads = []

        gevent_threads.append(
            gevent.spawn(self.working)
        )

        w = self.working()
        w.send(None)
        for i in range(3):
            gevent_threads.append(
                gevent.spawn(self.crawling, w)
            )
        gevent.joinall(gevent_threads)
        end_time = datetime.now()
        print '用时 '+str(end_time-start_time)


# def main():
#     monkey.patch_socket()
#
#     cities = ['北京', '上海', '广州', '深圳', '杭州']
#     positions = ['python', 'java', 'php', 'c', 'c++']
#
#     for p in positions:
#         for c in cities:
#             task_queue.put((p, c, 1))
#
#     gevent_process()
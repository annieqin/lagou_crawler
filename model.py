# coding: utf-8

__author__ = 'AnnieQin <annie__qin@163.com>'

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
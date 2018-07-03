# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import time,json
from celery.schedules import crontab
from .models import CoefficientDetail
@shared_task(track_started=True)
def add(x, y):
    time.sleep(10)    #模拟长时间执行
    return x + y

@shared_task
def helpmsg():
    return "help msg"

@shared_task
def ensurerankleveltask():
    data = {}
    co = CoefficientDetail.objects.all()
    #更新用户系数返回结果写入日志logs/celery.log
    # for c in co:
    #     i, res = c.ensureranklevel()
    #     data[i] = res
    #     c.finalcoefficent()
    # json_str = json.dumps(data)
    count = 0
    for c in co:
        #更新等级系数及调增基数
        i, res = c.ensureranklevel()
        ai,ares = c.update_addbasesalary()
        #data[i] = res
        c.finalcoefficent()
        count = count + 1
    data["totalcount"] = count
    json_str = json.dumps(data)
    return json_str

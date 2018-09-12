# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import time,json
from .models import *
from coefficient.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q

from depart.models import DepartDetail
User = get_user_model()

@shared_task
def createbankquotacomplete(record):
    data = {}
    successcount = 0
    errcount = 0
    departs = DepartDetail.objects.filter(dept_type=2)
    for d in departs:
        try:
            quotas = Quota.objects.all()
            for q in quotas:
                bqc = BankQuotaComplete()
                bqc.performancerecord = record
                bqc.depart = d
                bqc.quota = q
                bqc.save()
            successcount = successcount+1
        except Exception as e:
            print(e)
            data[d.name] = str(e)
            errcount = errcount + 1
    data["successcount"] = successcount
    data["errcount"] = errcount
    json_str = json.dumps(data)
    return json_str




@shared_task
def createbankuploadrecord(record):
    data = {}
    successcount = 0
    errcount = 0
    departs = DepartDetail.objects.filter(dept_type=2)
    for d in departs:
        try:
            bur = BankUploadRecord()
            bur.performancerecord = record
            bur.depart = d
            bur.save()
            successcount = successcount+1
        except Exception as e:
            print(e)
            data[d.name] = str(e)
            errcount = errcount + 1
    data["successcount"] = successcount
    data["errcount"] = errcount
    json_str = json.dumps(data)
    return json_str

@shared_task
def createperformanceresults(record):
    data={}
    count = 0
    errcount = 0
    error = []
    departs = DepartDetail.objects.filter(dept_type=2)
    for depart in departs:
        users = User.objects.filter(user_depart__depart=depart)
        # print(users,len(users))
        for u in users:
            uco = CoefficientDetail.objects.get(user=u)
            upost = uco.rank13coefficent.post
            if upost:
                try:
                    pr = PerformanceResultDetail()
                    pr.perforrecord = record
                    pr.user = u
                    pr.depart = depart
                    pr.indexpostlevel = IndexPostLevel.objects.get(post=upost)
                    pr.save()
                    count = count + 1
                except Exception as e:
                    # print(ev.user.name)
                    # pass
                    error.append(u.name)
            else:
                errcount = errcount +1
                #data["LOCKED"] = "已经锁定评价控制开关，不在更新系数"
    data["errcount"] = errcount
    data["totalcount"] = count
    data["error"] = error
    json_str = json.dumps(data)
    return json_str


@shared_task
def updateperformanceresults():
    pass

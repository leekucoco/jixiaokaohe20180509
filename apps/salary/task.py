# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import time,json
from celery.schedules import crontab
from .models import FSalary,SalaryRecord
from django.contrib.auth import get_user_model
User = get_user_model()

@shared_task
def helpmsg():
    return "help msg"

@shared_task
def createsalaryrecord(salaryrecord):
    data = {}
    successcount = 0
    errcount = 0
    users = User.objects.all()
    for u in users:
        try:
            fs = FSalary()
            fs.user_id = u.id
            #fs.srecord = SalaryRecord.objects.get(id=salaryrecordid)
            fs.srecord = salaryrecord
            fs.idcardnumber = fs.getidcardnumber()
            fs.name = fs.getname()
            fs.depart = fs.getdepart()
            fs.post = fs.getpost()
            fs.joinedyears = fs.getjoinedyears()
            fs.yearsofworking = fs.getyearsofworking()
            fs.ywslary = fs.calcywslary()
            fs.education = fs.geteducation()
            fs.edslary = fs.calcedslary()
            fs.title = fs.gettitle()
            fs.tislary = fs.calctislary()
            fs.itrainer = fs.getittrainer()
            fs.itslary = fs.calcittrainersalary()
            fs.cmanagerrank =fs.getcmanagerrank()
            fs.cmslary = fs.calccmanagersalary()
            fs.fltotal = fs.gettotal()
            fs.rank = fs.getrank()
            fs.basesalary = fs.getbasesalary()
            fs.coefficent = fs.getcoefficent()
            fs.basesalarythismonth = fs.getbasesalarythismonth()
            fs.save()
            successcount = successcount + 1
        except Exception as e:
            data[u.username] = str(e)
            errcount = errcount + 1
    salaryrecord.status = "BASESALARYINITCOMPLETE"
    salaryrecord.save()
    data["successcount"] = successcount
    data["errcount"] = errcount
    json_str = json.dumps(data)
    return json_str

@shared_task
def destroysalaryrecord(instance):
    data = {}
    fsall = FSalary.objects.filter(srecord=instance)
    try:
        resultinfo = fsall.delete()
        data["successinfo"] = resultinfo
    except Exception as e:
        data["errinfo"] = e
    instance.delete()
    json_str = json.dumps(data)
    return json_str
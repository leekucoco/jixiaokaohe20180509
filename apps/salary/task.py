# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import time,json
from celery.schedules import crontab
from .models import FSalary,SalaryRecord
from django.db.models import Q
from django.contrib.auth import get_user_model
from openpyxl import load_workbook
User = get_user_model()
from extra_apps.YunPianMsgSender import YunPianMsg
from Dqrcbankjxkh.settings import APIKEY,TPLID

@shared_task
def updatesrecord():
    data = {}
    successcount = 0
    errcount = 0
    users = User.objects.all()
    for u in users:
        try:
            user_id = u.id
            srecord = SalaryRecord.objects.filter(~Q(status= 'LOCK'))
            if srecord:
                srecord = srecord[0]
                fs = FSalary.objects.get(user_id = user_id,srecord=srecord)
                fs.basesalaryresult = fs.calcbasesalaryreslut()
                fs.ywslary = fs.calcywslary()
                fs.edslary = fs.calcedslary()
                fs.tislary = fs.calctislary()
                fs.itslary = fs.calcittrainersalary()
                fs.cmslary = fs.calccmanagersalary()
                fs.fltotal = fs.gettotal()
                fs.welfareresult = fs.calcwelfareresult()
                fs.totalsalaryresult = fs.calctotalsalaryresult()
                fs.totalpayamount = fs.calctotalpayamount()
                fs.finalpayingamount = fs.calcfinalpayingamount()
                #print(fs)
                fs.save()
                successcount = successcount + 1
            else:
                data["status"] = "全部封账"
        except Exception as e:
            data[u.username] = str(e)
            errcount = errcount + 1
    data["successcount"] = successcount
    data["errcount"] = errcount
    json_str = json.dumps(data)
    return json_str


@shared_task
def sendmsg(id):
    ym = YunPianMsg(APIKEY,TPLID)
    # fsitem = {"mobile":"13329502095","name":"李晓龙","totalsalaryresult":"5300.21",
    # "totlainsuranceandfund":"897","performancepay":"10000","totalpayamount":"6700",
    # "finalpayingamount":"5678.32"}
    # cd = ym.yunpianmsg(**fsitem)
    # print(cd,id)
    data = {}
    successcount = 0
    errcount = 0
    u = User.objects.get(username = "510412")
    try:
        user_id = u.id
        user_mobile = u.mobile
        user_name = u.name
        srecord = SalaryRecord.objects.filter(id=id)
        if srecord:
            fsitem = {}
            srecord = srecord[0]
            fs = FSalary.objects.get(user_id = user_id,srecord=srecord)
            fsitem["mobile"] = user_mobile
            fsitem["name"] = user_name
            fsitem["basesalaryresult"] = fs.basesalaryresult
            fsitem["welfareresult"] = fs.welfareresult
            fsitem["totalsalaryresult"] = fs.totalsalaryresult
            fsitem["endowmentinsurance"] = fs.endowmentinsurance
            fsitem["medicalinsurance"] = fs.medicalinsurance
            fsitem["unemploymentinsurance"] = fs.unemploymentinsurance
            fsitem["housingprovidentfund"] = fs.housingprovidentfund
            fsitem["companyfund"] = fs.companyfund
            fsitem["totlainsuranceandfund"] = fs.totlainsuranceandfund
            fsitem["totalpayamount"] = fs.totalpayamount
            fsitem["personaltax"] = fs.personaltax
            fsitem["finalpayingamount"] = fs.finalpayingamount
            cd = ym.yunpianmsg(**fsitem)
            successcount = successcount + 1
        else:
            data["status"] = "无此记录"
    except Exception as e:
        data[u.username] = str(e)
        errcount = errcount + 1


    #users = User.objects.all()
    # for u in users:
    #     try:
    #         user_id = u.id
    #         user_mobile = u.mobile
    #         user_name = u.name
    #         srecord = SalaryRecord.objects.filter(id=id)
    #         if srecord:
    #             fsitem = {}
    #             srecord = srecord[0]
    #             fs = FSalary.objects.get(user_id = user_id,srecord=srecord)
    #             fsitem["mobile"] = user_mobile
    #             fsitem["name"] = user_name
    #             fsitem["basesalaryresult"] = fs.basesalaryresult
    #             fsitem["welfareresult"] = fs.welfareresult
    #             fsitem["totalsalaryresult"] = fs.totalsalaryresult
    #             fsitem["endowmentinsurance"] = fs.endowmentinsurance
    #             fsitem["medicalinsurance"] = fs.medicalinsurance
    #             fsitem["unemploymentinsurance"] = fs.unemploymentinsurance
    #             fsitem["housingprovidentfund"] = fs.housingprovidentfund
    #             fsitem["companyfund"] = fs.companyfund
    #             fsitem["totlainsuranceandfund"] = fs.totlainsuranceandfund
    #             fsitem["totalpayamount"] = fs.totalpayamount
    #             fsitem["personaltax"] = fs.personaltax
    #             fsitem["finalpayingamount"] = fs.finalpayingamount
    #             cd = ym.yunpianmsg(**fsitem)
    #             successcount = successcount + 1
    #         else:
    #             data["status"] = "无此记录"
    #     except Exception as e:
    #         data[u.username] = str(e)
    #         errcount = errcount + 1
    data["successcount"] = successcount
    data["errcount"] = errcount
    json_str = json.dumps(data)
    return json_str

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
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
def updatebankuploadrecorddetails():
    data={}
    count = 0
    errcount = 0
    error = []
    brds = BankUploadRecordDetail.objects.filter(burecord__state=4).exclude(burecord__performancerecord__state=2)
    if brds:
        try:
            for bd in brds:
                bd.score = bd.calcscore()
                bd.save()
                count = count + 1
        except Exception as e:
            errcount = errcount + 1
    else:
        error.append("no bankuploadrecorddetail !")
    data["errcount"] = errcount
    data["totalcount"] = count
    data["error"] = error
    json_str = json.dumps(data)
    return json_str



@shared_task
def updateperformanceresults():
    data={}
    count = 0
    errcount = 0
    error = []
    prs = PerformanceResultDetail.objects.filter(perforrecord__state=1)
    if prs:
        for p in prs:
            brds = BankUploadRecordDetail.objects.filter(user=p.user,burecord__performancerecord=p.perforrecord)
            if brds:
                for br in brds:
                    quoname = br.quota.name
                    if quoname == "对公存款日均额":
                        p.dgckrjplan = br.plan
                        p.dgckrjcomplete = br.complete
                        p.dgckrjscore = br.score
                    elif quoname == "零售存款日均额":
                        p.lsckrjplan = br.plan
                        p.lsckrjcomplete = br.complete
                        p.lsckrjscore = br.score
                    elif quoname == "对公贷款纯投放":
                        p.dgdkctfplan = br.plan
                        p.dgdkctfcomplete = br.complete
                        p.dgdkctfscore = br.score
                    elif quoname == "零售贷款纯投放":
                        p.lsdkctfplan = br.plan
                        p.lsdkctfcomplete = br.complete
                        p.lsdkctfscore = br.score
                    elif quoname == "到期贷款回收率":
                        p.dqdkhslplan = br.plan
                        p.dqdkhslcomplete = br.complete
                        p.dqdkhslscore = br.score
                    elif quoname == "利息回收":
                        p.lxhsplan = br.plan
                        p.lxhscomplete = br.complete
                        p.lxhsscore = br.score
                    elif quoname == "未进入不良的逾期贷款清收":
                        p.wjblqsplan = br.plan
                        p.wjblqscomplete = br.complete
                        p.wjblqsscore = br.score
                    elif quoname == "欠息贷款压降":
                        p.qxdkyjplan = br.plan
                        p.qxdkyjcomplete = br.complete
                        p.qxdkyjscore = br.score
                    elif quoname == "表内不良资产处置":
                        p.bnblzcczplan = br.plan
                        p.bnblzcczcomplete = br.complete
                        p.bnblzcczscore = br.score
                    elif quoname == "表外不良资产处置":
                        p.bwblzcczplan = br.plan
                        p.bwblzcczcomplete = br.complete
                        p.bwblzcczscore = br.score
                    elif quoname == "业务笔数":
                        p.ywamount = br.complete
                    else:
                        errcount = errcount +1
                    p.save()
            else:
                error.append("no burecords")
    else:
        error.append("no PerformanceResultDetail! all record locked")
    data["errcount"] = errcount
    data["totalcount"] = count
    data["error"] = error
    json_str = json.dumps(data)
    return json_str

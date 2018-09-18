# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import time,json
from .models import *
from coefficient.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db.models import Avg, Sum, Max, Min, Count

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
        # print(len(brds))
        try:
            for bd in brds:
                # print(bd.user,bd.quota)
                bd.score = bd.calcscore()
                # print("{}--{}--{}".format(bd.user,bd.quota,bd.score))
                bd.save()
                count = count + 1
        except Exception as e:
            errcount = errcount + 1
            print(e)
    else:
        error.append("no bankuploadrecorddetail !")
    data["errcount"] = errcount
    data["totalcount"] = count
    data["error"] = error
    json_str = json.dumps(data)
    return json_str



@shared_task
def updateperformancescore():
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
                        pass

            else:
                errcount = errcount + 1
                # error.append(p.user.name)
            p.totalscore = p.dgckrjscore + p.lsckrjscore + p.dgdkctfscore + p.lsdkctfscore +\
            p.dqdkhslscore + p.lxhsscore +  p.wjblqsscore + p.qxdkyjscore +  p.bnblzcczscore + p.bwblzcczscore
            p.save()
    else:
        error.append("no PerformanceResultDetail! all record locked")
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
    # sumdgckrjscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('dgckrjscore'))
    # sumlsckrjscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('lsckrjscore'))
    # sumdgdkctfscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('dgdkctfscore'))
    # sumlsdkctfscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('lsdkctfscore'))
    # sumdqdkhslscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('dqdkhslscore'))
    # sumlxhsscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('lxhsscore'))
    # sumwjblqsscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('wjblqsscore'))
    # sumqxdkyjscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('qxdkyjscore'))
    # sumbnblzcczscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('bnblzcczscore'))
    # bwblzcczscore = PerformanceResultDetail.objects.filter(perforrecord__state=1).aggregate(Sum('bwblzcczscore'))

    # print(sumdgckrjscore,sumlsckrjscore,sumdgdkctfscore,
    #       sumlsdkctfscore,sumdqdkhslscore,sumlxhsscore,
    #       sumwjblqsscore,sumqxdkyjscore,sumbnblzcczscore,bwblzcczscore)
    ywbseachmoney = 0
    prds = PerformanceResultDetail.objects.filter(perforrecord__state=1).order_by("-id")
    if prds:
        prd = prds[0]
        splitmethod = prd.perforrecord.splitmethod
        #临桂人员总额
        linguimenberstotalmoney = splitmethod.linguimenberstotalmoney
        # 客户经理总额
        custmorsertotalmoney = splitmethod.custmorsertotalmoney
        ywbseachmoney = splitmethod.ywbsmoney
        accountingsupervisormoney = linguimenberstotalmoney * splitmethod.accountingsupervisor
        # print(accountingsupervisormoney)
        vpointernalmoney = linguimenberstotalmoney * splitmethod.vpointernal
        clerkmoney = linguimenberstotalmoney * splitmethod.clerk
        custmorsermanagermoney = custmorsertotalmoney * splitmethod.custmorsermanager
        vpofieldmoney = custmorsertotalmoney * splitmethod.custmorsermanager
        creditgeneralmoney = custmorsertotalmoney * splitmethod.custmorsermanager
        presidentmoney = custmorsertotalmoney * splitmethod.custmorsermanager
    else:
        accountingsupervisormoney,vpointernalmoney,clerkmoney,custmorsermanagermoney,\
        vpofieldmoney,creditgeneralmoney,presidentmoney = 0,0,0,0,0,0,0

    sumxdzhscore = PerformanceResultDetail.objects.filter\
        (perforrecord__state=1,indexpostlevel__splitlevel__name="信贷综合").aggregate(Sum('totalscore'))
    sumxdzhscore = sumxdzhscore['totalscore__sum']
    sumkhjlscore = PerformanceResultDetail.objects.filter\
        (perforrecord__state=1,indexpostlevel__splitlevel__name="客户经理").aggregate(Sum('totalscore'))
    sumkhjlscore = sumkhjlscore['totalscore__sum']
    sumnqptygscore = PerformanceResultDetail.objects.filter\
        (perforrecord__state=1,indexpostlevel__splitlevel__name="内勤普通员工").aggregate(Sum('totalscore'))
    sumnqptygscore = sumnqptygscore['totalscore__sum']
    sumnqfhzscore = PerformanceResultDetail.objects.filter\
        (perforrecord__state=1,indexpostlevel__splitlevel__name="内勤副行长").aggregate(Sum('totalscore'))
    sumnqfhzscore = sumnqfhzscore['totalscore__sum']
    sumwqfhzscore = PerformanceResultDetail.objects.filter\
        (perforrecord__state=1,indexpostlevel__splitlevel__name="外勤副行长").aggregate(Sum('totalscore'))
    sumwqfhzscore = sumwqfhzscore['totalscore__sum']
    sumhzscore = PerformanceResultDetail.objects.filter\
        (perforrecord__state=1,indexpostlevel__splitlevel__name="行长").aggregate(Sum('totalscore'))
    sumhzscore = sumhzscore['totalscore__sum']
    sumkjzgscore = PerformanceResultDetail.objects.filter\
        (perforrecord__state=1,indexpostlevel__splitlevel__name="会计主管").aggregate(Sum('totalscore'))
    sumkjzgscore = sumkjzgscore['totalscore__sum']

    # print(sumxdzhscore)
    kjzgsmoneyscore = accountingsupervisormoney / sumkjzgscore if sumkjzgscore !=0 else 0
    hzmoneyscore = presidentmoney / sumhzscore if sumhzscore !=0 else 0
    wqfhzmoneyscore = vpofieldmoney / sumwqfhzscore if sumwqfhzscore != 0 else 0
    nqfhzmoneysocre = vpointernalmoney / sumnqfhzscore if sumnqfhzscore != 0 else 0
    nqptygmoneyscore = clerkmoney / sumnqptygscore if sumnqptygscore != 0 else 0
    khjlmoneyscore = custmorsermanagermoney / sumkhjlscore if sumkhjlscore != 0 else 0
    xdzhmoneyscore = creditgeneralmoney / sumxdzhscore if sumxdzhscore != 0 else 0

    # print(kjzgsmoneyscore,hzmoneyscore,wqfhzmoneyscore,nqfhzmoneysocre,nqptygmoneyscore,khjlmoneyscore,xdzhmoneyscore)

    prs = PerformanceResultDetail.objects.filter(perforrecord__state=1)
    if prs:
        for pr in prs:
            if pr.indexpostlevel.splitlevel.name == "信贷综合":
                pr.scoremoney = pr.totalscore * xdzhmoneyscore
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            elif pr.indexpostlevel.splitlevel.name == "客户经理":
                pr.scoremoney = pr.totalscore * khjlmoneyscore
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            elif pr.indexpostlevel.splitlevel.name == "内勤普通员工":
                pr.scoremoney = pr.totalscore * nqptygmoneyscore
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            elif pr.indexpostlevel.splitlevel.name == "内勤副行长":
                pr.scoremoney = pr.totalscore * nqfhzmoneysocre
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            elif pr.indexpostlevel.splitlevel.name == "外勤副行长":
                pr.scoremoney = pr.totalscore * wqfhzmoneyscore
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            elif pr.indexpostlevel.splitlevel.name == "行长":
                pr.scoremoney = pr.totalscore * hzmoneyscore
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            elif pr.indexpostlevel.splitlevel.name == "会计主管":
                pr.scoremoney = pr.totalscore * kjzgsmoneyscore
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            else:
                pr.scoremoney = -1
                pr.ywamountmoney = pr.ywamount * ywbseachmoney
                pr.totalmoney = pr.scoremoney + pr.ywamountmoney
            # print(pr.user.name,pr.scoremoney,pr.ywamountmoney,pr.totalmoney)
            pr.save()
            count = count + 1
    else:
        error.append("no PerformanceResultDetail! all record locked")
    data["errcount"] = errcount
    data["totalcount"] = count
    data["error"] = error
    json_str = json.dumps(data)
    return json_str
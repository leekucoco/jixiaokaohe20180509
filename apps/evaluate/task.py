# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import time,json
from celery.schedules import crontab
from .models import AppraisalTicket,AppraisalProcedure,EvaluateResult
from depart.models import DepartDetail,IndexUserDepart
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()


@shared_task
def refreshevaluateresult():
    data={}
    count = 0
    errcount = 0
    departs = DepartDetail.objects.filter(dept_type=1)
    for depart in departs:
        users = User.objects.filter(user_depart__depart=depart)
        for u in users:
            ev = EvaluateResult.objects.filter(user=u, evaluateoftheyear__state="UNLOCK")
            #print(ev,type(ev))
            if ev:
                try:
                    ev = ev[0]
                    departmanagersocre,bankleaderscore = ev.get_departleaderandmanagerscore()
                    ev.departleaderscore = departmanagersocre
                    ev.bankleadersocre = bankleaderscore
                    ev.leaderevaluatescore = ev.get_leaderevaluatescore()
                    ev.qualificationsscore = ev.get_qualificationsscore()
                    ev.democraticappraisalscore = ev.get_democraticappraisalscore()
                    ev.ceoresult = ev.get_level(ev.ceoscore)
                    ev.departleaderesult = ev.get_level(departmanagersocre)
                    ev.bankleaderresult = ev.get_level(bankleaderscore)
                    ev.leaderevaluate = ev.get_level(ev.leaderevaluatescore)
                    ev.democraticappraisal = ev.get_level(ev.democraticappraisalscore)
                    ev.qualifications = ev.get_level(ev.qualificationsscore)
                    ev.save()
                    count = count + 1
                except Exception as e:
                    data["error"] = ev.user.name
            else:
                errcount = errcount +1
                #data["LOCKED"] = "已经锁定评价控制开关，不在更新系数"
    data["errcount"] = errcount
    data["totalcount"] = count
    json_str = json.dumps(data)
    return json_str





@shared_task
def createevaluateresult(record):
    data = {}
    successcount = 0
    errcount = 0
    users = User.objects.all()
    for u in users:
        try:
            er = EvaluateResult()
            er.evaluateoftheyear = record
            er.user = u
            er.save()
            successcount = successcount+1
        except Exception as e:
            print(e)
            data[u.name] = str(e)
            errcount = errcount + 1
    record.save()
    data["successcount"] = successcount
    data["errcount"] = errcount
    json_str = json.dumps(data)
    return json_str




@shared_task
def createprocedurerecord(record):
    if record.appraisalchoices == "DEMOCRATICAPPRAISAL":
        data = {}
        successcount = 0
        errcount = 0
        departs = DepartDetail.objects.filter(dept_type=1)
        departs = departs.exclude(name__in=["副行级", "领导班子"])
        for depart in departs:
            try:
                users = User.objects.filter(user_depart__depart=depart)
                #print(users)
                if depart.manager:
                    for u in users.exclude(id = depart.manager.id):
                        for ap in users.exclude(id__in=[u.id, depart.manager.id]):
                            #print(u, users.exclude(id=u.id))
                            ticket = AppraisalTicket()
                            ticket.appraisalprocedure = record
                            ticket.evaluateperson = u
                            ticket.appraisedperson = ap
                            ticket.save()
                            successcount = successcount + 1
                else:
                    for u in users:
                        for ap in users.exclude(id=u.id):
                            #print(u, users.exclude(id=u.id))
                            ticket = AppraisalTicket()
                            ticket.appraisalprocedure = record
                            ticket.evaluateperson = u
                            ticket.appraisedperson = ap
                            ticket.save()
                            successcount = successcount + 1
            except Exception as e:
                print(e)
                data[depart.name] = str(e)
                errcount = errcount + 1
        record.save()
        data["successcount"] = successcount
        data["errcount"] = errcount
        json_str = json.dumps(data)
        return json_str
    elif record.appraisalchoices == "LEADERVALUATE":
        data = {}
        successcount = 0
        errcount = 0
        departs = DepartDetail.objects.filter(dept_type=1)
        departs = departs.exclude(name__in=["副行级", "领导班子"])
        for depart in departs:
            try:
                users = User.objects.filter(user_depart__depart=depart)
                #print(users)
                if depart.manager and depart.leader:
                    for u in users.exclude(id = depart.manager.id):
                        #print(users.exclude(id = depart.manager.id), depart.manager, u)
                        ticket = AppraisalTicket()
                        ticket.appraisalprocedure = record
                        ticket.evaluateperson = depart.manager
                        ticket.appraisedperson = u
                        ticket.save()
                        successcount = successcount + 1
                    for u in users:
                        ticket = AppraisalTicket()
                        ticket.appraisalprocedure = record
                        ticket.evaluateperson = depart.leader
                        ticket.appraisedperson = u
                        ticket.save()
                        successcount = successcount + 1
                else:
                    pass
            except Exception as e:
                print(e)
                data[depart.name] = str(e)
                errcount = errcount + 1
        # 董事长评价用纸质评价，人事部门负责
        # ceogroup = Group.objects.get(name="董事长")
        # ceouser = User.objects.get(groups=ceogroup)
        # ceoevaluategroup = Group.objects.get(name="董事长评价用户组")
        # ceoevaluateusers = User.objects.filter(groups=ceoevaluategroup)
        # for u in ceoevaluateusers:
        #     ticket = AppraisalTicket()
        #     ticket.appraisalprocedure = record
        #     ticket.evaluateperson = ceouser
        #     ticket.appraisedperson = u
        #     ticket.save()
        #     successcount = successcount + 1
        record.save()
        data["successcount"] = successcount
        data["errcount"] = errcount
        json_str = json.dumps(data)
        return json_str
    elif record.appraisalchoices == "QUALIFICATIONS":
        pass
    else:
        pass



@shared_task
def destroyprocedurerecord(instance):
    data = {}
    fsall = AppraisalTicket.objects.filter(appraisalprocedure=instance)
    try:
        resultinfo = fsall.delete()
        data["successinfo"] = resultinfo
    except Exception as e:
        data["errinfo"] = e
    instance.delete()
    json_str = json.dumps(data)
    return json_str
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task,task
import time,json
from .models import *
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

# @shared_task
# def createprocedurerecord(record):
#     if record.appraisalchoices == "DEMOCRATICAPPRAISAL":
#         data = {}
#         successcount = 0
#         errcount = 0
#         departs = DepartDetail.objects.filter(dept_type=1)
#         departs = departs.exclude(name__in=["副行级", "领导班子"])
#         for depart in departs:
#             try:
#                 users = User.objects.filter(user_depart__depart=depart)
#                 #print(users)
#                 if depart.manager:
#                     for u in users.exclude(id = depart.manager.id):
#                         for ap in users.exclude(id__in=[u.id, depart.manager.id]):
#                             #print(u, users.exclude(id=u.id))
#                             ticket = AppraisalTicket()
#                             ticket.appraisalprocedure = record
#                             ticket.evaluateperson = u
#                             ticket.appraisedperson = ap
#                             ticket.save()
#                             successcount = successcount + 1
#                 else:
#                     for u in users:
#                         for ap in users.exclude(id=u.id):
#                             #print(u, users.exclude(id=u.id))
#                             ticket = AppraisalTicket()
#                             ticket.appraisalprocedure = record
#                             ticket.evaluateperson = u
#                             ticket.appraisedperson = ap
#                             ticket.save()
#                             successcount = successcount + 1
#             except Exception as e:
#                 print(e)
#                 data[depart.name] = str(e)
#                 errcount = errcount + 1
#         record.save()
#         data["successcount"] = successcount
#         data["errcount"] = errcount
#         json_str = json.dumps(data)
#         return json_str
#     elif record.appraisalchoices == "LEADERVALUATE":
#         data = {}
#         successcount = 0
#         errcount = 0
#         departs = DepartDetail.objects.filter(dept_type=1)
#         departs = departs.exclude(name__in=["副行级", "领导班子"])
#         for depart in departs:
#             try:
#                 users = User.objects.filter(user_depart__depart=depart)
#                 #print(users)
#                 if depart.manager and depart.leader:
#                     for u in users.exclude(id = depart.manager.id):
#                         #print(users.exclude(id = depart.manager.id), depart.manager, u)
#                         ticket = AppraisalTicket()
#                         ticket.appraisalprocedure = record
#                         ticket.evaluateperson = depart.manager
#                         ticket.appraisedperson = u
#                         ticket.save()
#                         successcount = successcount + 1
#                     for u in users:
#                         ticket = AppraisalTicket()
#                         ticket.appraisalprocedure = record
#                         ticket.evaluateperson = depart.leader
#                         ticket.appraisedperson = u
#                         ticket.save()
#                         successcount = successcount + 1
#                 else:
#                     pass
#             except Exception as e:
#                 print(e)
#                 data[depart.name] = str(e)
#                 errcount = errcount + 1
#         # 董事长评价用纸质评价，人事部门负责
#         # ceogroup = Group.objects.get(name="董事长")
#         # ceouser = User.objects.get(groups=ceogroup)
#         # ceoevaluategroup = Group.objects.get(name="董事长评价用户组")
#         # ceoevaluateusers = User.objects.filter(groups=ceoevaluategroup)
#         # for u in ceoevaluateusers:
#         #     ticket = AppraisalTicket()
#         #     ticket.appraisalprocedure = record
#         #     ticket.evaluateperson = ceouser
#         #     ticket.appraisedperson = u
#         #     ticket.save()
#         #     successcount = successcount + 1
#         record.save()
#         data["successcount"] = successcount
#         data["errcount"] = errcount
#         json_str = json.dumps(data)
#         return json_str
#     elif record.appraisalchoices == "QUALIFICATIONS":
#         pass
#     else:
#         pass



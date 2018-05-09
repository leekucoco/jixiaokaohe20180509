# -*- coding: utf-8
from django.db import models
from datetime import datetime,date
from  decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from depart.models import DepartDetail,IndexUserDepart
User = get_user_model()


class Evaluate(models.Model):
    STATE_CHOICES = (
        ("UNLOCK", "未锁定"),
        ("LOCK", "锁定"),
    )
    name = models.CharField(max_length=18, null=True, blank=True, verbose_name="年度测评",
                                      help_text="年度测评")
    state = models.CharField(null=True, blank=True, choices=STATE_CHOICES, default="UNLOCK", max_length=60,
                              verbose_name="测评状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")
    class Meta:
        verbose_name = "年度测评"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name



class AppraisalProcedure(models.Model):
    EVALUATE_CHOICES = (
        ("QUALIFICATIONS", "任职资格测评"),
        ("DEMOCRATICAPPRAISAL", "民主测评"),
        ("LEADERVALUATE", "有权人测评"),
    )
    evaluateoftheyear = models.ForeignKey(Evaluate, null=True, blank=True,verbose_name="年度测评",related_name="procedure_evaluate")
    name = models.CharField(max_length=60, null=True, blank=True, verbose_name="测评程序",
                                      help_text="测评程序")
    appraisalchoices = models.CharField(null=True, blank=True, choices=EVALUATE_CHOICES,  max_length=60,
                              verbose_name="测评种类")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")
    class Meta:
        verbose_name = "测评程序"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class AppraisalTicket(models.Model):
    appraisalprocedure = models.ForeignKey(AppraisalProcedure, verbose_name="测评程序",related_name= "appraisalticket_appraisalprocedure")
    evaluateperson = models.ForeignKey(User, verbose_name="评价人", related_name="eval_person")
    appraisedperson = models.ForeignKey(User, verbose_name="被评价人", related_name="appraise_person")
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="测评得分", help_text="测评得分")
    qualifications = models.CharField(max_length=18, null=True, blank=True, verbose_name="测评结果",
                                      help_text="测评结果")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")
    class Meta:
        verbose_name = "测评票"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.evaluateperson.name+"--"+self.appraisedperson.name

class EvaluateResult(models.Model):
    evaluateoftheyear = models.ForeignKey(Evaluate, null=True, blank=True,verbose_name="年度测评",related_name="result_evaluate")
    user = models.ForeignKey(User, verbose_name="用户")
    ceoscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True, verbose_name="董事长给分", help_text="董事长给分")
    departleaderscore= models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True, verbose_name="部门领导给分", help_text="部门领导给分")
    bankleadersocre= models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True, verbose_name="主管行长给分", help_text="主管行长给分")
    ceoresult = models.CharField(max_length=18, null=True, blank=True, verbose_name="董事长给分结果",
                                      help_text="董事长给分结果")
    departleaderesult = models.CharField(max_length=18, null=True, blank=True, verbose_name="部门领导给分结果",
                                      help_text="部门领导给分结果")
    bankleaderresult = models.CharField(max_length=18, null=True, blank=True, verbose_name="主管行长给分结果",
                                      help_text="主管行长给分结果")

    qualificationsscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True, verbose_name="任职资格测评得分", help_text="任职资格测评得分")
    democraticappraisalscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True, verbose_name="民主测评得分", help_text="民主测评得分")
    leaderevaluatescore =models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True, verbose_name="有权人测评得分", help_text="有权人测评得分")
    qualifications = models.CharField(max_length=18, null=True, blank=True, verbose_name="任职资格测评结果",
                                      help_text="任职资格测评结果")
    democraticappraisal = models.CharField(max_length=18, null=True, blank=True, verbose_name="民主测评结果",
                                           help_text="民主测评结果")
    leaderevaluate = models.CharField(max_length=18, null=True, blank=True, verbose_name="有权人测评结果",
                                      help_text="有权人测评结果")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")
    class Meta:
        verbose_name = "评价结果"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user.username

    #获取部门领导，主管行长给分
    def get_departleaderandmanagerscore(self):
        departinfo = DepartDetail.objects.filter(depart_user__user=self.user)
        if departinfo:
            depart = departinfo[0]
            departmanager = depart.manager
            rc = AppraisalTicket.objects.filter(appraisedperson=self.user, evaluateperson=departmanager,
                                                appraisalprocedure__evaluateoftheyear=self.evaluateoftheyear)
            if rc:
                departmanagerscore =  rc[0].score
            else:
                departmanagerscore = 0
            departleader = depart.leader

            rc2 = AppraisalTicket.objects.filter(appraisedperson=self.user, evaluateperson=departleader,
                                                appraisalprocedure__evaluateoftheyear=self.evaluateoftheyear)
            if rc2:
                departleaderscore =  rc2[0].score
            else:
                departleaderscore = 0
        else:
            departmanagerscore = 0
            departleaderscore = 0
        return departmanagerscore, departleaderscore

    def get_level(self,score):
        if score == 0:
            return "未评价"
        elif 0<score <70:
            return "较差"
        elif 70<=score<80:
            return "一般"
        elif 80<=score<90:
            return "良好"
        elif 90<=score<=100:
            return "优秀"
        else:
            return "错误结果"
    def get_qualificationsscore(self):
        return Decimal(90)


    def get_democraticappraisalscore(self):
        return Decimal(90)

    def get_leaderevaluatescore(self):
        ceoevaluategroup = Group.objects.get(name="董事长评价用户组")
        ceoevaluateusers = User.objects.filter(groups=ceoevaluategroup)
        if self.user in ceoevaluateusers:
            leaderevaluatescore = (self.ceoscore+self.bankleadersocre)/Decimal(2)
            return leaderevaluatescore
        else:
            leaderevaluatescore = (self.bankleadersocre+self.departleaderscore)/Decimal(2)
            return leaderevaluatescore

        # ceoevaluateusersid = []
        # departs = DepartDetail.objects.filter(dept_type=1)
        # countnormal,countnormalerr,countceoevaluate = 0,0,0

        # for u in ceoevaluateusers:
        #     ev = EvaluateResult.objects.get(user=u,evaluateoftheyear=self.evaluateoftheyear)
        #     bankleaderscore = self.bankleadersocre
        #     leaderevaluatescore = (self.ceoscore+bankleaderscore)/Decimal(2)
        #     print(ev,bankleaderscore,leaderevaluatescore,self.ceoscore)
        #     ev.leaderevaluatescore= leaderevaluatescore
        #     ev.save()
        #     countceoevaluate = countceoevaluate+1
        #     ceoevaluateusersid.append(u.id)
        # #print(ceoevaluateusersid)
        # for depart in departs:
        #     try:
        #         users = User.objects.filter(user_depart__depart=depart)
        #         normalusers = users.exclude(id__in=ceoevaluateusersid)
        #         for u in normalusers:
        #             ev = EvaluateResult.objects.get(user=u,evaluateoftheyear=self.evaluateoftheyear)
        #             departmanagersocre,bankleaderscore = self.departleaderscore,self.bankleadersocre
        #
        #             leaderevaluatescore = (departmanagersocre+bankleaderscore)/Decimal(2)
        #             print(depart,ev,departmanagersocre,bankleaderscore,leaderevaluatescore)
        #             ev.leaderevaluatescore = leaderevaluatescore
        #             ev.save()
        #             countnormal = countnormal +1
        #     except Exception as e:
        #         countnormalerr = countnormalerr +1
        #         print(e)
        #
        # return {"countnormal":countnormal,"countceoevaluate":countceoevaluate,"countnormalerr":countnormalerr}

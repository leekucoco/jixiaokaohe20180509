# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.db import models
from datetime import datetime,date
from  decimal import Decimal
# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()
from rank13.models import Rank13Coefficent,Rank13Demands
from certificates.models import IndexUserCertificate
from depart.models import IndexUserDepart
class CoefficientDetail(models.Model):
    """
    系数明细
    """
    user = models.OneToOneField(User, verbose_name=u"用户")
    rank13demands = models.ForeignKey(Rank13Demands,  verbose_name=u"岗位等级及岗位要求", default=1)
    rank13coefficent = models.ForeignKey(Rank13Coefficent, verbose_name=u"等级行员关联系数", default=1)

    coefficent = models.DecimalField(max_digits=4,decimal_places=2,default=0,
                                     verbose_name="系数",help_text="系数")
    addbasesalary = models.DecimalField(max_digits=10,decimal_places=2,default=0,
                                     verbose_name="调增基本薪酬基数", help_text="调增基本薪酬基数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")
    is_special = models.BooleanField(default=False,verbose_name="是否为特殊指定系数")
    is_specialaddbasesalary = models.BooleanField(default=False, verbose_name="是否特殊调增基数")
    is_suspandwelfaresalary = models.BooleanField(default=False, verbose_name="是否停发福利薪酬")
    basesalary = models.DecimalField(max_digits=10,decimal_places=2,default=0,
                                     verbose_name="特殊基本薪酬", help_text="特殊基本薪酬")
    is_sepcialbasesalary = models.BooleanField(default=False, verbose_name="是否指定基础薪酬")
    class Meta:
        verbose_name = "员工系数"
        verbose_name_plural = verbose_name
        unique_together = ("user", "coefficent")

    def __str__(self):
        return self.user.username


    def update_addbasesalary(self):
        rank = self.rank13demands.rank
        if self.is_specialaddbasesalary == False:
            if rank <= 6:
                self.addbasesalary = Decimal(1000)
            elif 7 <= rank <= 8:
                self.addbasesalary = Decimal(1500)
            elif rank == 9:
                self.addbasesalary = Decimal(2000)
            elif rank == 10:
                self.addbasesalary = Decimal(3000)
            elif rank == 11:
                self.addbasesalary = Decimal(5000)
            elif rank == 12:
                self.addbasesalary = Decimal(6000)
            elif rank == 13:
                self.addbasesalary = Decimal(7000)
            else:
                self.addbasesalary = 0
            self.save()
            return  self.user.username, "成功更新用户等级系数"
        elif self.is_specialaddbasesalary == True:
            return self.user.username, "特殊调增基数，无法更改"
        else:
            pass





    def get_yearsofwork(self):#获取工作年限
        if self.user.joinedyears:
            return date.today().year-self.user.joinedyears.year
        elif self.user.joinedyears is None:
            return 0
        else:
            return 0
    def get_demandyears(self):#获取要求工作年限
        return self.rank13demands.demandyears
    def get_scoreofyears(self):#获取年限得分
        demands = self.get_demandyears()
        yearsofwork = self.get_yearsofwork()
        if yearsofwork == demands:
            return 0
        elif yearsofwork > demands:
            return int((yearsofwork-demands)/2)
        elif yearsofwork < demands:
            return (yearsofwork-demands)*2
    def get_education(self):#获取学历
        return self.user.education
    def get_demandeducation(self):#学历要求
        return self.rank13demands.educationdemands
    def get_scoreofeducation(self):#学历得分
        education = self.get_education()
        demandeducation = self.get_demandeducation()
        return education-demandeducation
    def get_title(self):#职称
        return self.user.title
    def get_demandtitle(self):#职称要求
        return self.rank13demands.titledemands
    def get_scoreoftitle(self):#职称得分
        title =self.get_title()
        demandtitle = self.get_demandtitle()
        return title - demandtitle
    def get_primccbp(self):#初级银行从业
        return self.user.primccbp
    def get_demandprimccbp(self):#初级银行从业要求
        return self.rank13demands.primccbpdemands
    def get_scoreofprimccbp(self):#初级银行从业得分
        primccbp = self.get_primccbp()
        demandprimccbp = self.get_demandprimccbp()
        return primccbp-demandprimccbp
    def get_intermediateccbp(self):#中级银行从业
        return self.user.intermediateccbp
    def get_scoreofintermediateccbp(self):
        return self.get_intermediateccbp()*2
    def get_internel_trainer(self):#内训师
        return self.user.internel_trainer
    def get_scoreofinternel_trainer(self):
        return self.get_internel_trainer()-1

    def get_certificatetotalscore(self):
        certificateinfo = IndexUserCertificate.objects.filter(user=self.user)
        scoret = 0
        if certificateinfo:
            for cer in certificateinfo:
                scoret = cer.certificate.score + scoret

        else:
            scoret = 0
        return scoret

    def get_total_score(self):
        rank = self.rank13demands.rank
        totalscore = 0
        scoreofyears = self.get_scoreofyears()
        scoreofeducation = self.get_scoreofeducation()
        scoreoftitle = self.get_scoreoftitle()
        scoreofprimccbp = self.get_scoreofprimccbp()
        scoreofintermediateccbp = self.get_scoreofintermediateccbp()
        scoreofinternel_trainer = self.get_scoreofinternel_trainer()
        certificatetotalscore = self.get_certificatetotalscore()
        totalscore = (scoreofyears+scoreofeducation+scoreofprimccbp+scoreoftitle+
                      scoreofintermediateccbp+scoreofinternel_trainer+
                      certificatetotalscore)

        return totalscore
    def get_level(self):#级次
        totalscore = self.get_total_score()
        level = 1
        if totalscore <= -10:
            level = 1
        elif -10< totalscore <= -5:
            level = 2
        elif -5 <totalscore <5:
            level = 3
        elif 5<= totalscore< 10:
            level = 4
        elif 10 <= totalscore:
            level = 5
        else :
            level = 0
        return level

    def ensureranklevel(self):
        rank = self.rank13demands.rank
        level = self.get_level()
        post = self.rank13demands.post
        agent = self.rank13demands.agent
        if self.is_special == False:
            co = Rank13Coefficent.objects.get(level=level, rank=rank, agent=agent,post=post)
            if self.rank13coefficent != co:
                self.rank13coefficent = co
                self.save()
                return  self.user.username, "成功更新用户等级系数"
            else:
                return self.user.username, "等级系数匹配无需更改"

        elif self.is_special == True:
            return self.user.username, "特殊等级系数用户无法更改"
        else:
            pass

    def finalcoefficent(self):
        cmanagerlevel =  self.user.cmanagerlevel
        cmanagerrank  =  self.user.cmanagerrank
        clerkrank     =  self.user.clerkrank
        depttype = 1
        try:
            depttypet = IndexUserDepart.objects.get(user=self.user)
            depttype =depttypet.depart.dept_type
            deptname = depttypet.depart.name
        except Exception as e:
            print(self.user.name,e)
        cm = [[2, 2, 1.6],[2, 3, 1.8], [2, 4, 2.0],
              [3, 2, 2.2],[3, 3, 2.4], [3, 4, 2.6],
              [4, 2, 2.8],[4, 3, 3.0], [4, 4, 3.2],
              [5, 2, 3.8],[5, 3, 3.8], [5, 4, 3.8],
              [5, 1, 3.8]
              ]

        cl = [[3,1.5],[4,1.7],[5,1.9],[6,1.9]]

        if self.is_special == False:
            #无论机关支行都用最高计算系数
            # 机关零售，公司，三农，战发 有客户经理不住
            if depttype == 1 :
                if deptname not in ["零售金融部","公司金融部","三农研发部","战略发展部","小微中心"]:
                    self.coefficent = self.rank13coefficent.coefficent
                else:
                    coe = 0
                    if clerkrank == 1 and cmanagerrank > 1:  # 客户经理系数判断
                        for i in cm:
                            if i[0] == cmanagerrank:
                                if i[1] == cmanagerlevel:
                                    coe = i[2]
                                    if coe > self.rank13coefficent.coefficent:
                                        self.coefficent = coe
                                    else:
                                        self.coefficent = self.rank13coefficent.coefficent
                                    # print("客户经理",coe)
                                    break
                                else:
                                    continue
                            else:
                                continue
                   #大于 见习柜员才有柜员等级
                    elif cmanagerrank == 1 and clerkrank > 2:
                        for i in cl:
                            if i[0] == clerkrank:
                                coe = i[1]
                                if coe > self.rank13coefficent.coefficent:
                                    self.coefficent = coe
                                else:
                                    self.coefficent = self.rank13coefficent.coefficent
                                # print("柜员",coe)
                                break
                            else:
                                continue
                    else:
                        self.coefficent = self.rank13coefficent.coefficent

            elif depttype==2 :
                coe = 0
                if clerkrank ==1 and cmanagerrank > 1:#客户经理系数判断
                    for i in cm:
                        if i[0] == cmanagerrank:
                            if i[1] == cmanagerlevel:
                                coe = i[2]
                                if coe > self.rank13coefficent.coefficent:
                                    self.coefficent = coe
                                else:
                                    self.coefficent = self.rank13coefficent.coefficent
                                #print("客户经理",coe)
                                break
                            else:
                                continue
                        else:
                            continue

                # 大于 见习柜员才有柜员等级
                elif cmanagerrank ==1 and clerkrank > 2:
                    for i in cl:
                        if i[0] == clerkrank:
                            coe = i[1]
                            if coe > self.rank13coefficent.coefficent:
                                self.coefficent = coe
                            else:
                                self.coefficent = self.rank13coefficent.coefficent
                            #print("柜员",coe)
                            break
                        else:
                            continue
                else:
                    self.coefficent = self.rank13coefficent.coefficent
            else:
                self.coefficent = self.rank13coefficent.coefficent
           #print("其他默认系数",self.coefficent)
            self.save()
        else:
            pass

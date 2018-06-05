# -*- coding: utf-8
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from coefficient.models import CoefficientDetail
from datetime import datetime,date
from depart.models import IndexUserDepart
from rank13.models import Rank13Coefficent
from coefficient.models import CoefficientDetail
from users.models import UserProfile
# Create your models here.
class SalaryRecord(models.Model):
    SALARYRECORD_STATUS = (
        ("UNCOMPELTE","尚未完成本月工资核算"),
        ("BASESALARYINITCOMPLETE", "已生成基础工资与福利薪酬"),
        ("CHECKONWORKATTENDANCECOMPLETE", "完成考勤录入"),
        ("TOTALSALARYCOMPLETE", "已生成薪酬合计"),
        ("INSURANCEANDFUNDCOMPELTE", "已经录入五险一金并生成应发薪酬"),
        ("TAXANDOTHERDEDUCTIONS", "已完成税费及其他扣除项录入生成实发薪酬"),
        ("LOCK", "封账"),
    )
    user = models.ForeignKey(User, verbose_name="用户")
    extrainfo = models.TextField(null=True,blank=True,verbose_name="备注",default=str(date.today().month)+"月工资记录")
    date = models.DateField(default=date.today, verbose_name="记录日期")
    checkonworkfile = models.FileField(null=True,blank=True,upload_to="salarybase", verbose_name="病假事假记录", help_text="病假事假记录")
    baseandwelfareaddfile = models.FileField(null=True,blank=True,upload_to="salarybase", verbose_name="补发基本福利薪酬记录",
                                             help_text="补发基本福利薪酬记录")
    insuranceandfundfile = models.FileField(null=True,blank=True,upload_to="salarybase", verbose_name="五险一金记录", help_text="五险一金记录")
    taxandotherdeductionfile = models.FileField(null=True,blank=True,upload_to="salarybase", verbose_name="税费及其他扣除项记录",
                                                help_text="税费及其他扣除项记录")
    status =  models.CharField(null=True,blank=True,choices=SALARYRECORD_STATUS, default="UNCOMPELTE", max_length=60, verbose_name="工资记录状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")
    class Meta:
        verbose_name = "月工资记录"

        verbose_name_plural = verbose_name

    def __str__(self):
        return self.extrainfo

class FSalary(models.Model):
    srecord = models.ForeignKey(SalaryRecord, verbose_name="月工资记录")
    user = models.ForeignKey(User, verbose_name=u"用户")
    idcardnumber = models.CharField(max_length=18, null=True, blank=True, verbose_name="身份证号")
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    depart = models.CharField(max_length=60, null=True, blank=True, verbose_name="机构")
    post = models.CharField(null=True, blank=True, max_length=60, verbose_name="岗位")
    joinedyears = models.DateField(null=True, blank=True, verbose_name="参加工作年月")
    yearsofworking = models.IntegerField(null=True,blank=True,default=1,verbose_name="工龄")
    ywslary = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="工龄津贴")
    education = models.CharField(max_length=30,null=True,blank=True,verbose_name="学历")
    edslary = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="学历津贴")
    title = models.CharField(max_length=30, null=True, blank=True, verbose_name="职称")
    tislary = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="职称津贴")
    itrainer = models.CharField(max_length=30, null=True, blank=True, verbose_name="内训师")
    itslary = models.DecimalField(max_digits=10, decimal_places=2, default=0,  verbose_name="内训师津贴")
    cmanagerrank = models.CharField(max_length=30, null=True, blank=True, verbose_name="客户经理级别")
    cmslary = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="客户经理津贴")
    fltotal = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="津贴合计")


    rank = models.IntegerField(default=1, verbose_name="行员等级",help_text="行员等级")
    coefficent = models.DecimalField(max_digits=4, decimal_places=2, default=0,
                                     verbose_name="系数", help_text="系数")
    basesalary = models.DecimalField(max_digits=10,decimal_places=2,default=0,
                                     verbose_name="基本薪酬基数", help_text="基本薪酬基数")
    basesalarythismonth = models.DecimalField(max_digits=10,decimal_places=2,default=0,
                                     verbose_name="基本薪酬", help_text="基本薪酬")
    privateaffairleavedays = models.IntegerField(default=0, verbose_name="事假天数",help_text="事假天数")
    sickleavedays = models.IntegerField(default=0, verbose_name="病假天数", help_text="病假天数")
    basesalarythismonthwithleaves = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                              verbose_name="基本薪酬病事假扣除", help_text="基本薪酬病事假扣除")
    basesalaryresult = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                              verbose_name="基本薪酬结果", help_text="基本薪酬结果")
    welfareresult = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="福利薪酬结果", help_text="福利薪酬结果")
    basesalaryadd = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                              verbose_name="补发基本薪酬", help_text="补发基本薪酬")
    welfareresultadd = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="补发福利薪酬", help_text="补发福利薪酬")
    totalsalaryresult = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="薪酬合计", help_text="薪酬合计")
    endowmentinsurance = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="养老保险", help_text="养老保险")
    medicalinsurance = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="医疗保险", help_text="医疗保险")
    unemploymentinsurance = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="失业保险", help_text="失业保险")
    housingprovidentfund = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="住房公积金", help_text="住房公积金")
    totlainsuranceandfund = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="三险一金合计", help_text="三险一金合计")
    totalpayamount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="应发薪酬", help_text="应发薪酬")
    personaltax = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="个人所得税", help_text="个人所得税")
    partymemberdues = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="代扣党费", help_text="代扣党费")
    otherdeductions = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="其他扣除项", help_text="其他扣除项")
    finalpayingamount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name="实发薪酬", help_text="实发薪酬")


    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "工资明细"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

    def getidcardnumber(self):
        return self.user.idcardnumber
    def getname(self):
        return self.user.name
    def getdepart(self):
        dept = IndexUserDepart.objects.filter(user=self.user)
        if dept:
            return dept[0].depart.name
        else:
            return "无"
    def getpost(self):
        rc = CoefficientDetail.objects.filter(user=self.user)
        if rc:
            return rc[0].rank13coefficent.post.name
        else:
            return "无"
    def getjoinedyears(self):
        return self.user.joinedyears

    def getyearsofworking(self):#获取工作年限
        if self.user.joinedyears:
            return date.today().year-self.user.joinedyears.year
        elif self.user.joinedyears is None:
            return 0
        else:
            return 0

    def calcywslary(self):
        yearsofworking = self.getyearsofworking()
        if yearsofworking<20:
            return yearsofworking*15
        elif yearsofworking>=20:
            return yearsofworking*20
        else:
            return 0
    def geteducation(self):
        edid = self.user.education
        ed = UserProfile.EDUCATION_CHOICES[edid-1]
        return ed
    def calcedslary(self):
        edid = self.user.education
        edsalary = 0
        if edid ==1:
            edsalary = 0
        elif edid == 2:
            edsalary = 100
        elif edid ==3:
            edsalary = 200
        elif edid == 4:
            edsalary = 300
        elif edid == 5:
            edsalary = 400
        else:
            edsalary = 0
        return edsalary
    def gettitle(self):
        tiid =  self.user.title
        ti = UserProfile.TITLE_CHOICES[tiid-1]
        return ti
    def calctislary(self):
        tiid = self.user.title
        tisalary = 0
        if tiid == 1:
            tisalary = 0
        elif tiid == 2:
            tisalary = 100
        elif tiid ==3:
            tisalary=200
        elif tiid ==4:
            tisalary=600
        else:
            tisalary = 0
        return tisalary
    def getittrainer(self):
        itid =  self.user.internel_trainer
        it = UserProfile.INTERNEL_TRAINER_CHOICES[itid-1]
        return it
    def calcittrainersalary(self):
        itid = self.user.internel_trainer
        itsalary = 0
        if itid == 1:
            itsalary = 0
        elif itid == 2:
            itsalary = 300
        elif itid == 3:
            itsalary = 600
        elif itid == 4:
            itsalary = 1000
        else:
            itsalary = 0
        return itsalary
    def getcmanagerrank(self):
        cmrankid = self.user.cmanagerrank
        cm = UserProfile.CMANAGERRANK_CHOICES[cmrankid-1]
        return cm

    def calccmanagersalary(self):
        cmrankid = self.user.cmanagerrank
        cmanagersalary = 0
        if cmrankid == 1:
            cmanagersalary = 0
        elif cmrankid == 2:
            cmanagersalary = 500
        elif cmrankid == 3:
            cmanagersalary = 1000
        elif cmrankid ==4 :
            cmanagersalary = 1500
        elif cmrankid ==5:
            cmanagersalary = 2000
        else:
            cmanagersalary=0
        return cmanagersalary

    def gettotal(self):
        ysalary = self.calcywslary()
        edsalary =self.calcedslary()
        titlesalary = self.calctislary()
        ittrainersalary =self.calcittrainersalary()
        cmanagersalary =self.calccmanagersalary()
        return ysalary+edsalary+titlesalary+ittrainersalary+cmanagersalary

    def getrank(self):
        rc = CoefficientDetail.objects.filter(user=self.user)
        if rc:
            return rc[0].rank13coefficent.rank
        else:
            return 1
    def getcoefficent(self):
        rc = CoefficientDetail.objects.filter(user=self.user)
        if rc:
            return rc[0].coefficent
        else:
            return 0
    def getbasesalary(self):
        dept = IndexUserDepart.objects.filter(user=self.user)
        if dept:
            return dept[0].depart.basesalary
        else:
            return 0

    def getbasesalarythismonth(self):
        co = self.getcoefficent()
        bs = self.getbasesalary()
        return co*bs



    def calcbasesalaryreslut(self):

        return self.basesalarythismonth-self.basesalarythismonthwithleaves

    def calcwelfareresult(self):
        return self.gettotal()

    def calctotalsalaryresult(self):
        bsr = self.calcbasesalaryreslut()
        wsr = self.calcwelfareresult()
        bsadd = self.basesalaryadd
        wsadd = self.welfareresultadd
        return bsr+wsr+bsadd+wsadd
    def calctotalpayamount(self):
        tr = self.calctotalsalaryresult()
        tif = self.totlainsuranceandfund
        return tr+tif

    def calcfinalpayingamount(self):
        tpa = self.calctotalpayamount()
        pt = self.personaltax
        pmd = self.partymemberdues
        ot = self.otherdeductions
        return tpa - pt- pmd -ot


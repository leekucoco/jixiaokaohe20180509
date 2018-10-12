from django.db import models
from datetime import datetime
from rank13.models import Post
from depart.models import DepartDetail
from coefficient.models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from  decimal import Decimal
class SplitLevel(models.Model):
    """
    分配层级
    """
    name = models.CharField(default="", unique=True, max_length=30, verbose_name="层级名称", help_text="层级名称")
    desc = models.TextField(default="", verbose_name="层级描述", help_text="层级描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "层级"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class IndexPostLevel(models.Model):
    """
    层级岗位对应关系

    """
    KIND_CHOICES=(
        (1, "临柜条线"),
        (2, "客户经理条线"),
    )
    kind = models.IntegerField(default=1, choices=KIND_CHOICES, verbose_name="分配条线", help_text="分配条线")
    post = models.ForeignKey(Post, related_name='split_post',verbose_name="岗位",on_delete=models.CASCADE)
    splitlevel =models.ForeignKey(SplitLevel, related_name='split_level',verbose_name="层级",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")
    class Meta:
        verbose_name = '层级岗位'
        verbose_name_plural = verbose_name
        unique_together = ("post", "splitlevel")

    def __str__(self):
        return self.post.name+"|"+self.splitlevel.name


class SplitMethod(models.Model):
    """
    分配方案
    """
    info = models.CharField(default="", max_length=30, verbose_name="分配方案", help_text="分配方案")
    totalmoney= models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="奖励总金额", help_text="奖励总金额")
    linguimenberstotalmoney = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="临柜人员奖励总金额", help_text="临柜人员奖励总金额")
    custmorsertotalmoney = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="客户经理奖励总金额", help_text="客户经理奖励总金额")
    accountingsupervisor = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name="会计主管层占比", help_text="会计主管层占比")
    vpointernal = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name="内勤副行长层占比", help_text="内勤副行长层占比")
    clerk = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name="内勤副普通员工层占比", help_text="内勤副普通员工层占比")
    custmorsermanager = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name="客户经理层占比", help_text="客户经理层占比")
    vpofield = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="外勤副行长",
                                            help_text="外勤副行长")
    creditgeneral = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="信贷综合",
                                            help_text="信贷综合")
    president = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="行长层占比",
                                            help_text="行长层占比")
    # level = models.ForeignKey(SplitLevel, related_name='split_level',verbose_name="层级",on_delete=models.CASCADE)
    ywbsmoney = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="业务笔数单价",help_text="业务笔数单价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "分配方案"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.info


class PerformanceRecord(models.Model):
    """
    绩效考核记录
    """
    STATE_CHOICES=(
        (1, "未封账"),
        (2, "已封账"),
    )
    info = models.CharField(default="", max_length=30, verbose_name="绩效考核信息", help_text="绩效考核信息")
    splitmethod = models.ForeignKey(SplitMethod, null= True,blank=True,verbose_name="分配方案", help_text="分配方案",
                                    related_name="performance_splitmethod",on_delete=models.CASCADE)
    state = models.IntegerField(default=1, choices=STATE_CHOICES, verbose_name="状态", help_text="状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "绩效考核记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.info

class Quota(models.Model):
    """
    指标
    """
    name = models.CharField(default="", max_length=30, verbose_name="指标名称", help_text="指标名称")
    desc = models.TextField(default="", verbose_name="指标描述", help_text="指标描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "指标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class BankQuotaComplete(models.Model):
    """
    支行指标完成情况
    """
    performancerecord = models.ForeignKey(PerformanceRecord, null= True,blank=True,verbose_name="绩效考核记录", help_text="绩效考核记录",
                                    related_name="bqc_performancerecord",on_delete=models.CASCADE)
    depart = models.ForeignKey(DepartDetail, null= True,blank=True,verbose_name="支行", help_text="支行",
                                    related_name="bqc_depart",on_delete=models.CASCADE)
    quota = models.ForeignKey(Quota, null= True,blank=True, related_name='bqc_quota', verbose_name="指标", on_delete=models.CASCADE)
    plan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="指标计划", help_text="指标计划")
    complete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="指标完成", help_text="指标完成")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "支行指标完成情况"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.performancerecord.info + "|" + self.depart.name

class BankUploadRecord(models.Model):
    """
    支行考核记录
    """
    STATE_CHOICES=(
        (1, "未上传"),
        (2, "已提交审核"),
        (3, "审核未通过"),
        (4, "审核通过"),
    )
    performancerecord = models.ForeignKey(PerformanceRecord, null= True,blank=True,verbose_name="绩效考核记录", help_text="绩效考核记录",
                                    related_name="bur_performancerecord",on_delete=models.CASCADE)
    depart = models.ForeignKey(DepartDetail, null= True,blank=True,verbose_name="支行", help_text="支行",
                                    related_name="bur_depart",on_delete=models.CASCADE)
    state = models.IntegerField(default=1, choices=STATE_CHOICES, verbose_name="状态", help_text="状态")
    # quotaandcomplete = models.ForeignKey(BankQuotaComplete,null= True,blank=True,verbose_name="指标完成情况", help_text="指标完成情况")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "支行考核记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.performancerecord.info+"|"+self.depart.name




class BankUploadRecordDetail(models.Model):
    """
    支行考核明细
    """

    burecord = models.ForeignKey(BankUploadRecord, null= True,blank=True,verbose_name="支行考核记录", help_text="支行考核记录",
                                    related_name="burd_record",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='burd_user', verbose_name="用户", on_delete=models.CASCADE)
    quota = models.ForeignKey(Quota, related_name='burd_quota', verbose_name="指标", on_delete=models.CASCADE)
    plan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="指标计划", help_text="指标计划")
    complete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="指标完成", help_text="指标完成")
    score = models.DecimalField(max_digits=6,decimal_places=2,default=0,verbose_name="得分", help_text="得分")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "支行考核明细"
        verbose_name_plural = verbose_name
        unique_together = ("burecord", "user", "quota")


    def __str__(self):
        return self.burecord.depart.name+"|"+self.user.name+"|"+str(self.score)

    def calcscore(self):

        #信贷综合员季度营销得分＝存款营销得分 * 50 % +本机构客户经理平均绩效得分 * 50 %
        #ucoe = CoefficientDetail.objects.get(user=self.user)
        # upost = ucoe.rank13coefficent.post
        # if upost != "信贷综合":
        if self.quota.name == "表外不良资产处置":
            if self.plan == 0:
                return 0
            else:
                if self.complete-self.plan < 0:
                    score = Decimal(15)*Decimal(self.complete/self.plan)
                    if score >= 0:
                        return score
                    else:
                        return 0
                elif self.complete - self.plan >= 0:
                    return Decimal(15)
                else:
                    print("error bwblzccz calc")
        elif self.quota.name == "表内不良资产处置":
            if self.plan == 0:
                return 0
            else:
                if self.complete-self.plan < 0:
                    score = Decimal(10)*Decimal(self.complete/self.plan)
                    if score >= 0:
                        return score
                    else:
                        return 0
                elif self.complete - self.plan >= 0:
                    return Decimal(10)
                else:
                    print("error bnblzccz calc")
        elif self.quota.name == "欠息贷款压降":
            if self.plan == 0:
                return 0
            else:
                if self.complete-self.plan < 0:
                    score = Decimal(20)*Decimal(self.complete/self.plan)
                    if score >= 0:
                        return score
                    else:
                        return 0
                elif self.complete - self.plan >= 0:
                    return Decimal(20)
                else:
                    print("error qxdkyj calc")
        elif self.quota.name == "未进入不良的逾期贷款清收":
            if self.plan == 0:
                return 0
            else:
                if self.complete-self.plan < 0:
                    score = Decimal(10)*Decimal(self.complete/self.plan)
                    if score >= 0:
                        return score
                    else:
                        return 0
                elif self.complete - self.plan >= 0:
                    return Decimal(10)
                else:
                    print("error wjrbldyqdkqs calc")
        elif self.quota.name == "利息回收":
            if self.plan == 0:
                return 0
            else:
                if self.complete-self.plan < 0:
                    return 0
                elif self.complete - self.plan >= 0:
                    score = Decimal(30)+Decimal((self.complete - self.plan)/self.plan)*Decimal(10)
                    if score >= 35:
                        return Decimal(35)
                    else:
                        return score
                else:
                    print("error lxhs calc")
        elif self.quota.name == "到期贷款回收率":
            if self.plan == 0:
                return 0
            else:
                if self.complete-self.plan < 0:
                    score = Decimal(25)-Decimal((self.plan - self.complete)/self.plan)*Decimal(100*12.5)
                    if score >= 0:
                        return score
                    else:
                        return 0
                elif self.complete - self.plan >= 0:
                    return Decimal(25)
                else:
                    print("error dqdkhsl calc")
        elif self.quota.name == "零售贷款纯投放":
            if self.plan == 0:
                return 0
            else:
                if self.complete<=0:
                    return 0
                else:
                    if self.complete-self.plan < 0:
                        return Decimal(self.complete/self.plan)*Decimal(30)
                    elif self.complete - self.plan >= 0:
                        score = Decimal(30)+Decimal((self.complete - self.plan)/self.plan)*Decimal(10)
                        if score >= 35:
                            return Decimal(35)
                        else:
                            return score
                    else:
                        print("error lsdkctf calc")
        elif self.quota.name == "对公贷款纯投放":
            if self.plan == 0:
                return 0
            else:
                if self.complete<=0:
                    return 0
                else:
                    if self.complete-self.plan < 0:
                        return Decimal(self.complete/self.plan)*Decimal(15)
                    elif self.complete - self.plan >= 0:
                        score = Decimal(15)+Decimal((self.complete - self.plan)/self.plan)*Decimal(10)
                        if score >= 20:
                            return Decimal(20)
                        else:
                            return score
                    else:
                        print("error dgdkctf calc")
        elif self.quota.name == "零售存款日均额":
            if self.plan == 0:
                return 0
            else:
                if self.complete<=0:
                    return 0
                else:
                    if self.complete-self.plan < 0:
                        return Decimal(self.complete/self.plan)*Decimal(25)
                    elif self.complete - self.plan >= 0:
                        score = Decimal(25)+Decimal((self.complete - self.plan)/self.plan)*Decimal(10)
                        if score >= 30:
                            return Decimal(30)
                        else:
                            return score
                    else:
                        print("error lsckrj calc")
        elif self.quota.name == "对公存款日均额":
            if self.plan == 0:
                return 0
            else:
                if self.complete<=0:
                    return 0
                else:
                    if self.complete-self.plan < 0:
                        return Decimal(self.complete/self.plan)*Decimal(20)
                    elif self.complete - self.plan >= 0:
                        score = Decimal(20)+Decimal((self.complete - self.plan)/self.plan)*Decimal(10)
                        if score >= 25:
                            return Decimal(25)
                        else:
                            return score
                    else:
                        print("error dgrje calc")
        else:
            return 0
        # elif upost == "信贷综合":
        #     pds = BankUploadRecordDetail.objects.filter(burecord=self.burecord).exclude(user=self.user)
        #     if pds:
        #         sumscore = 0
        #         for p in pds:
        #             sumscore = sumscore + p.score
        #         avgscore = sumscore/len(pds)
        #     else:
        #         avgscore = 0
        #     pdcunkuans= BankUploadRecordDetail.objects.filter(burecord=self.burecord,user=self.user,quota__name__in=["零售存款日均额","对公存款日均额"])
        #     if pdcunkuans:
        #         sumcunkuan = 0
        #         for c in pdcunkuans:
        #             sumcunkuan = sumcunkuan + c.score
        #         avgcunkuanscore = sumcunkuan/len(pdcunkuans)
        #     else:
        #         avgcunkuanscore = 0
        #     return (avgscore+avgcunkuanscore)*Decimal(0.5)

        # else:
        #     print(self.user)
        #     pds = BankUploadRecordDetail.objects.filter(burecord=self.burecord).exclude(user=self.user)
        #     if pds:
        #         sumscore = 0
        #         for p in pds:
        #             sumscore = sumscore + p.score
        #         avgscore = sumscore/len(pds)
        #     else:
        #         avgscore = 0
        #     pdcunkuans= BankUploadRecordDetail.objects.filter(burecord=self.burecord,user=self.user,quota__name__in=["零售存款日均额","对公存款日均额"])
        #     if pdcunkuans:
        #         sumcunkuan = 0
        #         for c in pdcunkuans:
        #             sumcunkuan = sumcunkuan + c.score
        #         avgcunkuanscore = sumcunkuan/len(pdcunkuans)
        #     else:
        #         avgcunkuanscore = 0
        #     return (avgscore+avgcunkuanscore)*Decimal(0.5)





class PerformanceResultDetail(models.Model):
    """
    考核结果明细
    """

    perforrecord = models.ForeignKey(PerformanceRecord, null= True,blank=True,verbose_name="考核记录", help_text="考核记录",
                                    related_name="perresult_record",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='perresult_user', verbose_name="用户", on_delete=models.CASCADE)
    depart = models.CharField(default="", max_length=30, verbose_name="部门", help_text="部门")
    indexpostlevel = models.ForeignKey(IndexPostLevel, related_name='perresult_indexpostlevel', verbose_name="用户-分配层级", on_delete=models.CASCADE)
    dgckrjplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="对公存款日均额计划", help_text="对公存款日均额计划")
    dgckrjcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="对公存款日均额完成", help_text="对公存款日均额完成")
    dgckrjscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="对公存款日均额得分", help_text="对公存款日均额得分")
    lsckrjplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="零售存款日均额计划", help_text="零售存款日均额计划")
    lsckrjcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="零售存款日均额完成", help_text="零售存款日均额完成")
    lsckrjscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="零售存款日均额得分", help_text="零售存款日均额得分")
    dgdkctfplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="对公贷款纯投放计划", help_text="对公贷款纯投放计划")
    dgdkctfcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="对公贷款纯投放完成", help_text="对公贷款纯投放完成")
    dgdkctfscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="对公贷款纯投放得分", help_text="对公贷款纯投放得分")
    lsdkctfplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="零售贷款纯投放计划", help_text="零售贷款纯投放计划")
    lsdkctfcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="零售贷款纯投放完成", help_text="零售贷款纯投放完成")
    lsdkctfscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="零售贷款纯投放得分", help_text="零售贷款纯投放得分")
    dqdkhslplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="到期贷款回收率计划", help_text="到期贷款回收率计划")
    dqdkhslcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="到期贷款回收率完成", help_text="到期贷款回收率完成")
    dqdkhslscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="到期贷款回收率得分", help_text="到期贷款回收率得分")
    lxhsplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="利息回收计划", help_text="利息回收计划")
    lxhscomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="利息回收完成", help_text="利息回收完成")
    lxhsscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="利息回收得分", help_text="利息回收得分")
    wjblqsplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="未进入不良的逾期贷款清收计划", help_text="未进入不良的逾期贷款清收计划")
    wjblqscomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="未进入不良的逾期贷款清收完成", help_text="未进入不良的逾期贷款清收完成")
    wjblqsscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="未进入不良的逾期贷款清收得分", help_text="未进入不良的逾期贷款清收得分")
    qxdkyjplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="欠息贷款压降计划", help_text="欠息贷款压降计划")
    qxdkyjcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="欠息贷款压降完成", help_text="欠息贷款压降完成")
    qxdkyjscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="欠息贷款压降得分", help_text="欠息贷款压降得分")
    bnblzcczplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="表内不良资产处置计划", help_text="表内不良资产处置计划")
    bnblzcczcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="表内不良资产处置完成", help_text="表内不良资产处置完成")
    bnblzcczscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="表内不良资产处置得分", help_text="表内不良资产处置得分")
    bwblzcczplan = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="表外不良资产处置计划", help_text="表外不良资产处置计划")
    bwblzcczcomplete = models.DecimalField(max_digits=12,decimal_places=2,default=0,verbose_name="表外不良资产处置完成", help_text="表外不良资产处置完成")
    bwblzcczscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="表外不良资产处置得分", help_text="表外不良资产处置得分")
    ywamount = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="业务笔数", help_text="业务笔数")
    totalscore = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="总得分", help_text="总得分")
    scoremoney = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name="得分奖励金额", help_text="得分奖励金额")
    ywamountmoney = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="业务笔数奖励金额", help_text="业务笔数奖励金额")
    totalmoney = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="总奖励金额", help_text="总奖励金额")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "考核结果明细"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.user.name

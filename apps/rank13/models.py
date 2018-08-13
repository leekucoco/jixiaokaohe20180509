from django.db import models
from datetime import datetime
class Agent(models.Model):
    name = models.CharField(default="大庆农商银行", max_length=30,unique=True,
                            verbose_name="组织", help_text="组织")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "组织"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(default="", max_length=80, unique=True,
                            verbose_name="岗位", help_text="岗位")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "岗位"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Rank13Coefficent(models.Model):
    agent = models.ForeignKey(Agent, verbose_name="组织", help_text="组织", related_name="agent_rank13coefficent",on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="岗位", help_text="岗位", related_name="post_rank13coefficent",on_delete=models.CASCADE)
    rank = models.IntegerField(default=1, verbose_name="等次",
                                help_text="等次")
    level = models.IntegerField(default=1, verbose_name="级次",
                                help_text="级次")
    coefficent = models.DecimalField(max_digits=4,decimal_places=2,default=0,
                                     verbose_name="系数",help_text="系数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "行员等级对应岗位系数"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.agent.name+" "+self.post.name+" "+str(self.rank)+" "+str(self.level)+" "+str(self.coefficent)

class Rank13Demands(models.Model):
    EDUCATION_CHOICES = (
        (1, "高中（中专）及以下"),
        (2, "大学专科"),
        (3, "大学本科"),
        (4, "硕士研究生"),
        (5, "博士研究生及以上"),
    )
    TITLE_CHOICES = (
        (1, "无"),
        (2, "初级"),
        (3, "中级"),
        (4, "高级"),
    )
    INTERNEL_TRAINER_CHOICES = (
        (1, "无"),
        (2, "初级"),
        (3, "中级"),
        (4, "高级"),
    )
    CLERKRANK_CHONCES=(
        (1, "无"),
        (2, "见习柜员"),
        (3, "初级柜员"),
        (4, "中级柜员"),
        (5, "高级柜员"),
        (6, "资深柜员"),

    )
    CMANAGERLEVEL_CHOICES=(
        (1, "无"),
        (2, "一等"),
        (3, "二等"),
        (4, "三等"),
    )
    CMANAGERRANK_CHOICES=(
        (1, "无"),
        (2, "初级"),
        (3, "中级"),
        (4, "高级"),
    )

    #2.0测试增假ondelete
    agent = models.ForeignKey(Agent, verbose_name="组织", help_text="组织", related_name="agent_demand",on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="岗位", help_text="岗位", related_name="post_demand",on_delete=models.CASCADE)
    rank = models.IntegerField(default=1, verbose_name="等次",
                                help_text="等次")
    level = models.IntegerField(blank=True,null=True, verbose_name="级次",
                                help_text="级次")
    demandyears = models.IntegerField(default=1, verbose_name="金融从业年限要求",
                                help_text="金融从业年限要求")
    educationdemands  = models.IntegerField(default=1, choices=EDUCATION_CHOICES, verbose_name="学历",
                                      help_text=u"学历: 1高中（中专）及以下,2(大学专科),3(大学本科),4(硕士研究生),5(博士研究生及以上)")
    primccbpdemands = models.IntegerField(default=0, verbose_name="从业资格证书要求",
                                help_text="从业资格证书要求")
    titledemands = models.IntegerField(default=1, choices=TITLE_CHOICES, verbose_name="职称",
                                help_text=u"职称: 1(无),2(初级),3(中级),4(高级)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = "行员等级与任职资格要求"
        verbose_name_plural = verbose_name
        unique_together=("rank","level")
    def __str__(self):
        return self.agent.name+" "+self.post.name+" "+str(self.rank)+" "+str(self.level)
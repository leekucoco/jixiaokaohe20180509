# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date
from .models import CoefficientDetail
from depart.models import IndexUserDepart
from depart.serializers import DepartSerializer
from certificates.models import IndexUserCertificate
from certificates.serializers import IndexUserCertificateSerializer
from rank13.models import Rank13Coefficent

User = get_user_model()

class CofficientCreateSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    add_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = CoefficientDetail
        fields = "__all__"

class CofficientUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CoefficientDetail
        fields = "__all__"


class CoefficientDetailSerializer(serializers.ModelSerializer):

    add_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    idcardnumber = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    depart = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    rank13 = serializers.SerializerMethodField()
    joinedyears = serializers.SerializerMethodField()
    yearsofwork = serializers.SerializerMethodField()
    demandyears = serializers.SerializerMethodField()
    scoreofyears = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    demandeducation = serializers.SerializerMethodField()
    scoreofeducation = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    demandtitle = serializers.SerializerMethodField()
    scoreoftitle = serializers.SerializerMethodField()
    primccbp = serializers.SerializerMethodField()
    demandprimccbp = serializers.SerializerMethodField()
    scoreofprimccbp = serializers.SerializerMethodField()
    intermediateccbp = serializers.SerializerMethodField()
    scoreofintermediateccbp = serializers.SerializerMethodField()
    internel_trainer = serializers.SerializerMethodField()
    scoreofinternel_trainer = serializers.SerializerMethodField()
    totalscore = serializers.SerializerMethodField()
    certificates = serializers.SerializerMethodField()
    certificatetotalscore = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    r13coefficent = serializers.SerializerMethodField()
    class Meta:
        model = CoefficientDetail
        fields = ("id","user","rank13demands",
                  "name","idcardnumber","depart",
                  "post","rank13","joinedyears",
                  "yearsofwork","demandyears","scoreofyears",
                  "education","demandeducation","scoreofeducation",
                  "title","demandtitle","scoreoftitle",
                  "primccbp","demandprimccbp","scoreofprimccbp",
                  "intermediateccbp","scoreofintermediateccbp",
                  "internel_trainer","scoreofinternel_trainer","totalscore",
                  "certificates","certificatetotalscore","level",
                  "rank13coefficent","r13coefficent","coefficent","is_special",
                  "add_time","update_time"
                  )
    def get_r13coefficent(self,obj):
        return obj.rank13coefficent.coefficent
    def get_rank13(self,obj):
        return obj.rank13demands.rank
    def get_post(self,obj):
        return obj.rank13demands.post.name
    def get_depart(self,obj):
        departinfo = IndexUserDepart.objects.filter(user=obj.user)
        if departinfo:
            departinfod = departinfo[0].depart
            departinfo_serializer = DepartSerializer(departinfod, many=False, context={'request':self.context['request']})
            return departinfo_serializer.data
        else:
            return []
    def get_idcardnumber(self,obj):
        return obj.user.idcardnumber
    def get_name(self,obj):
        return obj.user.name

    def get_certificatetotalscore(self,obj):
        certificateinfo = IndexUserCertificate.objects.filter(user=obj.user)
        scoret = 0
        if certificateinfo:
            for cer in certificateinfo:
                scoret = cer.certificate.score + scoret
        else:
            scoret = 0
        # if obj.cscore != scoret:
        #     obj.cscore = scoret
        #     obj.save()
        # else :
        #     scoret =obj.cscore
        return scoret
    def get_certificates(self,obj):
        #all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        certificateinfo = IndexUserCertificate.objects.filter(user=obj.user)
        if certificateinfo:
            certificates_serializer = IndexUserCertificateSerializer(certificateinfo, many=True, context={'request': self.context['request']})
            return certificates_serializer.data
        else:
            return  "no certificates info"
    def get_joinedyears(self,obj):#获取参加工作时间
        return obj.user.joinedyears
    def get_yearsofwork(self,obj):#获取工作年限
        if obj.user.joinedyears:
            return date.today().year-obj.user.joinedyears.year
        elif obj.user.joinedyears is None:
            return 0
        else:
            return 0
    def get_demandyears(self,obj):#获取要求工作年限
        return obj.rank13demands.demandyears
    def get_scoreofyears(self,obj):#获取年限得分
        demands = self.get_demandyears(obj)
        yearsofwork = self.get_yearsofwork(obj)
        if yearsofwork == demands:
            return 0
        elif yearsofwork > demands:
            return round((yearsofwork-demands)/2)*1
        elif yearsofwork < demands:
            return (yearsofwork-demands)*2

    def get_education(self,obj):#获取学历
        return obj.user.education
    def get_demandeducation(self,obj):#学历要求
        return obj.rank13demands.educationdemands
    def get_scoreofeducation(self,obj):#学历得分
        education = self.get_education(obj)
        demandeducation = self.get_demandeducation(obj)
        return education-demandeducation
    def get_title(self,obj):#职称
        return obj.user.title
    def get_demandtitle(self,obj):#职称要求
        return obj.rank13demands.titledemands
    def get_scoreoftitle(self,obj):#职称得分
        title =self.get_title(obj)
        demandtitle = self.get_demandtitle(obj)
        return title - demandtitle
    def get_primccbp(self,obj):#初级银行从业
        return obj.user.primccbp
    def get_demandprimccbp(self,obj):#初级银行从业要求
        return obj.rank13demands.primccbpdemands
    def get_scoreofprimccbp(self,obj):#初级银行从业得分
        primccbp = self.get_primccbp(obj)
        demandprimccbp = self.get_demandprimccbp(obj)
        return primccbp-demandprimccbp
    def get_intermediateccbp(self,obj):#中级银行从业
        return obj.user.intermediateccbp
    def get_scoreofintermediateccbp(self,obj):
        return self.get_intermediateccbp(obj)*2
    def get_internel_trainer(self,obj):#内训师
        return obj.user.internel_trainer
    def get_scoreofinternel_trainer(self,obj):
        return self.get_internel_trainer(obj)-1
    def get_totalscore(self,obj):#总得分
        totalscore = 0
        scoreofyears = self.get_scoreofyears(obj)
        scoreofeducation = self.get_scoreofeducation(obj)
        scoreoftitle = self.get_scoreoftitle(obj)
        scoreofprimccbp = self.get_scoreofprimccbp(obj)
        scoreofintermediateccbp = self.get_scoreofintermediateccbp(obj)
        scoreofinternel_trainer = self.get_scoreofinternel_trainer(obj)
        certificatetotalscore = self.get_certificatetotalscore(obj)
        totalscore = (scoreofyears+scoreofeducation+scoreofprimccbp+scoreoftitle+
                      scoreofintermediateccbp+scoreofinternel_trainer+
                      certificatetotalscore)
        return totalscore

    def get_level(self,obj):#级次
        rank = self.get_rank13(obj)
        totalscore = self.get_totalscore(obj)
        level = 1
        if totalscore <= -10:
            level =  1
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

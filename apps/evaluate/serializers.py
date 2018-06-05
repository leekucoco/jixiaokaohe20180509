# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import AppraisalProcedure,AppraisalTicket,EvaluateResult,Evaluate

class EvaluateSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Evaluate
        fields = "__all__"




class AppraisalTicketSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    evaluatepersonname = serializers.SerializerMethodField()
    appraisedpersonname =serializers.SerializerMethodField()
    appraisalproceduretype = serializers.SerializerMethodField()
    def get_appraisalproceduretype(self,obj):
        if obj.appraisalprocedure.appraisalchoices=="DEMOCRATICAPPRAISAL":
            return "民主测评程序"
        elif obj.appraisalprocedure.appraisalchoices=="LEADERVALUATE":
            return "有权人测评程序"
        elif obj.appraisalprocedure.appraisalchoices=="QUALIFICATIONS":
            return "任职资格测评程序"

    def get_evaluatepersonname(self,obj):
        return obj.evaluateperson.name
    def get_appraisedpersonname(self,obj):
        return obj.appraisedperson.name
    class Meta:
        model = AppraisalTicket
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     #修改商品数量
    #     instance.checkonworkfile = validated_data["checkonworkfile"]
    #     instance.save()
    #     return instance

class AppraisalProcedureSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppraisalProcedure
        fields = "__all__"

class EvaluateResultSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self,obj):
        return obj.user.name
    class Meta:
        model = EvaluateResult
        fields = "__all__"
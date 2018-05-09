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
    class Meta:
        model = EvaluateResult
        fields = "__all__"
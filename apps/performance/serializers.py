# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import SplitLevel,IndexPostLevel,\
    SplitMethod,PerformanceRecord,Quota,BankQuotaComplete,BankUploadRecord,BankUploadRecordDetail
class SplitLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplitLevel
        fields = "__all__"

class IndexPostLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndexPostLevel
        fields = "__all__"

class SplitMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplitMethod
        fields = "__all__"

class PerformanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceRecord
        fields = "__all__"

class QuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = "__all__"
class BankQuotaCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankQuotaComplete
        fields = "__all__"
class BankUploadRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankUploadRecord
        fields = "__all__"
class BankUploadRecordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankUploadRecordDetail
        fields = "__all__"
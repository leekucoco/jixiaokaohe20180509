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
    performancerecord =serializers.PrimaryKeyRelatedField(read_only=True)
    depart=serializers.PrimaryKeyRelatedField(read_only=True)
    depart_info = serializers.SerializerMethodField()
    performancerecord_info = serializers.SerializerMethodField()
    def get_depart_info(self,obj):
        return obj.depart.name
    def get_performancerecord_info(self,obj):
        return obj.performancerecord.info
    class Meta:
        model = BankUploadRecord
        fields = "__all__"
class BankUploadRecordDetailSerializer(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    user_username=serializers.SerializerMethodField()
    quota_name = serializers.SerializerMethodField()
    def get_user_name(self,obj):
        return obj.user.name
    def get_user_username(self,obj):
        return obj.user.username
    def get_quota_name(self,obj):
        return obj.quota.name
    class Meta:
        model = BankUploadRecordDetail
        fields = "__all__"

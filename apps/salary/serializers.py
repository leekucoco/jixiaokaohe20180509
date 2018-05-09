# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import SalaryRecord, FSalary

class SalaryRecordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    date = serializers.DateField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SalaryRecord
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     #修改商品数量
    #     instance.checkonworkfile = validated_data["checkonworkfile"]
    #     instance.save()
    #     return instance


class FSlarySerializer(serializers.ModelSerializer):
    class Meta:
        model = FSalary
        fields = "__all__"
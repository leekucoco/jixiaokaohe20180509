# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import DepartDetail,IndexUserDepart
class DepartSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepartDetail
        fields = ("id","agent", "name", "dept_type", "parent_dept", "manager", "leader", "basesalary")

class IndexUserDepartSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndexUserDepart
        fields = "__all__"

    # def validate(self, attrs):
    #     attrs["add_time"] = self.generate_order_sn()
    #     return attrs
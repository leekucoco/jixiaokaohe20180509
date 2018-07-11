# -*- coding: utf-8 -*-
__author__ = 'bobby'
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime,date
from depart.models import DepartDetail,IndexUserDepart
from depart.serializers import DepartSerializer
from certificates.models import Cerficates,IndexUserCertificate
from certificates.serializers import CerficateSerializer,IndexUserCertificateSerializer
from datetime import timedelta
from rest_framework.validators import UniqueValidator
from django.db.models import Q
from django.utils.timezone import now
from Dqrcbankjxkh.settings import REGEX_MOBILE
from rank13.serializers import Rank13CoefficentSerializer
User = get_user_model()


# class SmsSerializer(serializers.Serializer):
#     mobile = serializers.CharField(max_length=11)
#
#     def validate_mobile(self, mobile):
#         """
#         验证手机号码
#         :param data:
#         :return:
#         """
#
#         # 手机是否注册
#         if User.objects.filter(mobile=mobile).count():
#             raise serializers.ValidationError("用户已经存在")
#
#         # 验证手机号码是否合法
#         if not re.match(REGEX_MOBILE, mobile):
#             raise serializers.ValidationError("手机号码非法")
#
#         # 验证码发送频率
#         one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
#         if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
#             raise serializers.ValidationError("距离上一次发送未超过60s")
#
#         return mobile



class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    depart_user = serializers.SerializerMethodField()

    certificates = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id","user", "idcardnumber", "username",  "name","depart_user",
                  "mobile","joinedyears", "workingyears", "education", "title", "internel_trainer",
                  "certificates",
                  "cmanagerlevel","cmanagerrank","clerkrank",
                  "primccbp","intermediateccbp","is_staff")

    def get_depart_user(self,obj):
        departinfo = IndexUserDepart.objects.filter(user_id=obj.id)
        if departinfo:
            departinfod = departinfo[0].depart
            departinfo_serializer = DepartSerializer(departinfod, many=False, context={'request':self.context['request']})
            return departinfo_serializer.data
        else:
            return "do not exist"

    def get_certificates(self,obj):
        #all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        certificateinfo = IndexUserCertificate.objects.filter(user_id=obj.id)
        if certificateinfo:
            #certificateinfod = certificateinfo._result_cache[0]
            certificates_serializer = IndexUserCertificateSerializer(certificateinfo, many=True, context={'request': self.context['request']})
            return certificates_serializer.data
        else:
            return  "no certificates info"
    def get_is_staff(self,obj):
        return obj.is_staff


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("__all__")
# class UserRegSerializer(serializers.ModelSerializer):
#     code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,label="验证码",
#                                  error_messages={
#                                      "blank": "请输入验证码",
#                                      "required": "请输入验证码",
#                                      "max_length": "验证码格式错误",
#                                      "min_length": "验证码格式错误"
#                                  },
#                                  help_text="验证码")
#     username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
#                                      validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
#
#     password = serializers.CharField(
#         style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
#     )
#
#     # def create(self, validated_data):
#     #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
#     #     user.set_password(validated_data["password"])
#     #     user.save()
#     #     return user
#


#     def validate_code(self, code):
#         # try:
#         #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
#         # except VerifyCode.DoesNotExist as e:
#         #     pass
#         # except VerifyCode.MultipleObjectsReturned as e:
#         #     pass
#         verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
#         if verify_records:
#             last_record = verify_records[0]
#             five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
#             if five_mintes_ago > last_record.add_time:
#                 raise serializers.ValidationError("验证码过期")
#             if last_record.code != code:
#                 raise serializers.ValidationError("验证码错误")
#         else:
#             raise serializers.ValidationError("验证码错误")
#
#     def validate(self, attrs):
#         attrs["mobile"] = attrs["username"]
#         del attrs["code"]
#         return attrs
#
#     class Meta:
#         model = User
#         fields = ("username", "code", "mobile", "password")

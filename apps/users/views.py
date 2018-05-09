from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from utils.permissions import IsSuperUser
from .serializers import  UserDetailSerializer, UserCreateSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
#     """
#     发送短信验证码
#     """
#     serializer_class = SmsSerializer
#
#     def generate_code(self):
#         """
#         生成四位数字的验证码
#         :return:
#         """
#         seeds = "1234567890"
#         random_str = []
#         for i in range(4):
#             random_str.append(choice(seeds))
#
#         return "".join(random_str)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         mobile = serializer.validated_data["mobile"]
#
#         yun_pian = YunPian(APIKEY)
#
#         code = self.generate_code()
#
#         sms_status = yun_pian.send_sms(code=code, mobile=mobile)
#
#         if sms_status["code"] != 0:
#             return Response({
#                 "mobile":sms_status["msg"]
#             }, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             code_record = VerifyCode(code=code, mobile=mobile)
#             code_record.save()
#             return Response({
#                 "mobile":mobile
#             }, status=status.HTTP_201_CREATED)
#

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class UserViewset(viewsets.ModelViewSet):
    """
    用户
    """
    # serializer_class = UserDetailSerializer
    permission_classes = (IsSuperUser,)
    queryset = User.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = UserPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'idcardnumber', 'username')
    ordering_fields = ('joinedyears', 'education')
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "list":
            return UserDetailSerializer
        return UserCreateSerializer

    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    # def get_permissions(self):
    #     if self.action == "retrieve":
    #         return [permissions.IsAdminUser()]
    #     elif self.action == "create":
    #         return [permissions.IsAdminUser()]
    #     elif self.action == "list":
    #         return [permissions.IsAdminUser()]
    #     elif self.action == "update":
    #         return [permissions.IsAdminUser()]
    #     elif self.action == "partial_update":
    #         return [permissions.IsAdminUser()]
    #     elif self.action == "destroy":
    #         return [permissions.IsAdminUser()]
    #     else:
    #         return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["password"] = "123456"
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

     # def get_object(self):
     #     return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        passwd = serializer.validated_data["password"]
        if serializer.validated_data["password"]:
            instance = self.get_object()
            instance.set_password(passwd)
            instance.save()
        else:
            serializer.save()

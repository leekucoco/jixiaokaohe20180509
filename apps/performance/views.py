# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import permissions
from utils.permissions import IsPerformanceAdminUser
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsSuperUser
from .models import *
from .serializers import  *
from depart.models import *
from rest_framework import filters
from django.contrib.auth.models import Group
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .task import createbankquotacomplete,createbankuploadrecord,createperformanceresults
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class PerformancePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class SplitLevelViewset(viewsets.ModelViewSet):
    """
    分配层级（2018）
    """
    serializer_class = SplitLevelSerializer
    queryset = SplitLevel.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('add_time',)
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsSuperUser()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsSuperUser()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

class IndexPostLevelViewset(viewsets.ModelViewSet):
    """
    层级岗位对应关系
    """
    serializer_class = IndexPostLevelSerializer
    queryset = IndexPostLevel.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('post__name','splitlevel__name')
    ordering_fields = ('post', 'add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsSuperUser()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsSuperUser()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]


class SplitMethodViewset(viewsets.ModelViewSet):
    """
    分配方案
    """
    serializer_class =  SplitMethodSerializer
    queryset =  SplitMethod.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("info",)
    ordering_fields = ('info', 'add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsSuperUser()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsSuperUser()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

class PerformanceRecordViewset(viewsets.ModelViewSet):
    """
    绩效考核记录
    """
    serializer_class =  PerformanceRecordSerializer
    queryset =  PerformanceRecord.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('info','splitmethod_info')
    ordering_fields = ('info', 'add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsSuperUser()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsSuperUser()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        record = serializer.save()
        createbankquotacomplete.delay(record)
        createbankuploadrecord.delay(record)
        createperformanceresults.delay(record)







class QuotaViewset(viewsets.ModelViewSet):
    """
    指标
    """
    serializer_class =  QuotaSerializer
    queryset =  Quota.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name', 'add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsPerformanceAdminUser()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsPerformanceAdminUser()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

class BankQuotaCompleteViewset(viewsets.ModelViewSet):
    """
    支行指标完成情况
    """
    serializer_class =  BankQuotaCompleteSerializer
    queryset =  BankQuotaComplete.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('performancerecord_info','depart_name','quota_name')
    ordering_fields = ('performancerecord','depart', 'add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsSuperUser()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsSuperUser()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

class BankUploadRecordViewset(viewsets.ModelViewSet):
    """
    支行考核记录
    """
    serializer_class =  BankUploadRecordSerializer
    # queryset =  BankUploadRecord.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('performancerecord_info','depart_name','state')
    ordering_fields = ('performancerecord','depart','state','quotaandcomplete', 'add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsPerformanceAdminUser()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsPerformanceAdminUser()]
        elif self.action == "update":
            return [IsPerformanceAdminUser()]
        elif self.action == "partial_update":
            return [IsPerformanceAdminUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        #return FSalary.objects.filter(user=self.request.user)
        burusergroup = Group.objects.get(name="基层绩效考核员")
        users = User.objects.filter(groups=burusergroup)
        if self.request.user.is_superuser:
            return BankUploadRecord.objects.all().order_by("id")
        elif self.request.user in users:
            # user = self.request.user
            # departs = IndexUserDepart.objects.filter(user=user)
            # print(departs)
            userdepart = self.request.user.user_depart.depart
            if userdepart:
                # depart = departs[0].depart
                return BankUploadRecord.objects.filter(depart=userdepart).exclude(performancerecord__state=2).order_by("-add_time")
            else:
                return "用户没有部门，请查证"
        else:
            return ""



class BankUploadRecordDetailViewset(viewsets.ModelViewSet):
    """
    支行考核明细
    """
    serializer_class =  BankUploadRecordDetailSerializer
    # queryset =  BankUploadRecordDetail.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PerformancePagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user_name','burecord_depart__name','user_username')
    ordering_fields = ('burecord','user','quota','plan', 'complete','score','add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [IsPerformanceAdminUser()]
        elif self.action == "create":
            return [IsPerformanceAdminUser()]
        elif self.action == "list":
            return [IsPerformanceAdminUser()]
        elif self.action == "update":
            return [IsPerformanceAdminUser()]
        elif self.action == "partial_update":
            return [IsPerformanceAdminUser()]
        elif self.action == "destroy":
            return [IsPerformanceAdminUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        #return FSalary.objects.filter(user=self.request.user)
        burusergroup = Group.objects.get(name="基层绩效考核员")
        users = User.objects.filter(groups=burusergroup)
        if self.request.user.is_superuser:
            return BankUploadRecordDetail.objects.all().order_by("id")
        elif self.request.user in users:
            # user = self.request.user
            # departs = IndexUserDepart.objects.filter(user=user)
            # print(departs)
            # userdepart = self.request.user.user_depart.depart
            # if departs:
            #     depart = departs[0].depart
            #     return BankUploadRecordDetail.objects.filter(burecord__depart=depart).exclude(burecord__state=4).order_by("-add_time")
            # else:
            #     return "用户没有部门，请查证"
            userdepart = self.request.user.user_depart.depart
            if userdepart:
                return BankUploadRecordDetail.objects.filter(burecord__depart=userdepart).exclude(burecord__state=4).order_by("-add_time")
            else:
                return "用户没有部门，请查证"
        else:
            return "用户不在考核管理员组"
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = self.request.user
        # departs = IndexUserDepart.objects.filter(user=user)
        userdepart = self.request.user.user_depart.depart
        if userdepart:
            # depart = departs[0].depart
            bur = BankUploadRecord.objects.filter(depart=userdepart)
            if bur:
                bur=bur[0]
                serializer.validated_data["burecord"] = bur
                self.perform_create(serializer)
                re_dict = serializer.data
                headers = self.get_success_headers(serializer.data)
                return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response("添加失败", status=status.HTTP_404_NOT_FOUND, headers=None)
        else:
            return Response("添加失败", status=status.HTTP_404_NOT_FOUND, headers=None)

     # def get_object(self):
     #     return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # user = self.request.user
        # departs = IndexUserDepart.objects.filter(user=user)
        userdepart = self.request.user.user_depart.depart
        if userdepart:
            # depart = departs[0].depart
            bur = BankUploadRecord.objects.filter(depart=userdepart)
            if bur:
                bur = bur[0]
                serializer.validated_data["burecord"] = bur
                self.perform_update(serializer)
                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
            else:
                return Response("添加失败", status=status.HTTP_404_NOT_FOUND, headers=None)
        else:
            return Response("添加失败", status=status.HTTP_404_NOT_FOUND, headers=None)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
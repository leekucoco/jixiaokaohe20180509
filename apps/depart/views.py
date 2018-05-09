
from django.contrib.auth import get_user_model

from rest_framework import viewsets

from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import DepartDetail,IndexUserDepart
from .serializers import  DepartSerializer,IndexUserDepartSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from utils.permissions import IsSuperUser


class DepartPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class DepartViewset(viewsets.ModelViewSet):
    """
    机构
    """
    serializer_class = DepartSerializer
    queryset = DepartDetail.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = DepartPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('name', 'basesalary')
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]


class IndexUserDepartPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class IndexUserDeparViewset(viewsets.ModelViewSet):
    """
    用户机构中间表
    """
    serializer_class = IndexUserDepartSerializer
    queryset = IndexUserDepart.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = IndexUserDepartPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__name', 'depart__name')
    ordering_fields = ('user__name', 'depart__name', 'add_time')
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action == "update":
            return [IsSuperUser()]
        elif self.action == "partial_update":
            return [IsSuperUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]


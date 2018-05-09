

from rest_framework import viewsets

from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsSuperUser

from .models import Rank13Coefficent,Agent,Post,Rank13Demands
from .serializers import  Rank13CoefficentSerializer,PostSerializer,\
    AgentSerializer,Rank13DemandsSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class Rank13CoefficentPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class Rank13CoefficentViewset(viewsets.ModelViewSet):
    """
    行员等级对应岗位系数标准（2018）
    """
    serializer_class = Rank13CoefficentSerializer
    queryset = Rank13Coefficent.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = Rank13CoefficentPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('agent__name','rank','post__name','level','coefficent')
    ordering_fields = ('rank', 'coefficent')
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
class Rank13DemandsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class Rank13DemandsViewset(viewsets.ModelViewSet):
    """
    行员等级与任职资格要求对照表
    """
    serializer_class = Rank13DemandsSerializer
    queryset = Rank13Demands.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = Rank13DemandsPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('post__name','agent__name','rank')
    ordering_fields = ('rank', 'post', 'agent')
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



class PostPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class PostViewset(viewsets.ModelViewSet):
    """
    岗位
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = PostPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name')
    ordering_fields = ('name', 'add_time')
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
class AgentPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class AgentViewset(viewsets.ModelViewSet):
    """
    组织
    """
    serializer_class = AgentSerializer
    queryset = Agent.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    pagination_class = AgentPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name')
    ordering_fields = ('name', 'add_time')
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
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from rest_framework.pagination import PageNumberPagination
from .serializers import AppraisalTicketSerializer,AppraisalProcedureSerializer,EvaluateResultSerializer,EvaluateSerializer
from .models import AppraisalTicket,AppraisalProcedure,EvaluateResult,Evaluate
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()
from .task import createprocedurerecord,destroyprocedurerecord,createevaluateresult
from datetime import datetime
from utils.permissions import IsSuperUser


class IsTicketOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.evaluateperson == request.user


class Pagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100

class AppraisalTicketViewset(viewsets.ModelViewSet):
    """
    测评票
    """
    #permission_classes = (IsAuthenticated, IsTicketOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AppraisalTicketSerializer
    pagination_class = Pagination

    def get_queryset(self):
        #return FSalary.objects.filter(user=self.request.user)
        if self.request.user.is_superuser:
            return AppraisalTicket.objects.filter(evaluateperson=self.request.user,appraisalprocedure__evaluateoftheyear__state="UNLOCK")
        # elif self.request.user.is_staff:
        #     userdepart = self.request.user.user_depart.depart
        #     users = User.objects.filter(user_depart__depart=userdepart)
        #     return AppraisalTicket.objects.filter(evaluateperson__in=users)
        else:
            return AppraisalTicket.objects.filter(evaluateperson=self.request.user,appraisalprocedure__evaluateoftheyear__state="UNLOCK")

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated(),IsTicketOwnerOrReadOnly()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [IsAuthenticated(),IsTicketOwnerOrReadOnly()]
        elif self.action == "update":
            return [IsTicketOwnerOrReadOnly()]
        elif self.action == "partial_update":
            return [IsTicketOwnerOrReadOnly()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [IsAuthenticated(),IsTicketOwnerOrReadOnly()]

class EvaluateResultViewset(viewsets.ModelViewSet):
    """
    测评结果
    """
    #permission_classes = (IsAuthenticated, IsTicketOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EvaluateResultSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('user__name', 'user__username')
    def get_queryset(self):
        #return FSalary.objects.filter(user=self.request.user)
        if self.request.user.is_superuser:
            return EvaluateResult.objects.all()
        else:
            return EvaluateResult.objects.filter(user=self.request.user)

    def get_permissions(self):
        return [IsSuperUser(),]


class AppraisalProcedureViewset(viewsets.ModelViewSet):
    """
    测评程序
    """
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AppraisalProcedureSerializer
    pagination_class = Pagination

    def perform_create(self, serializer):
        record = serializer.save()
        createprocedurerecord.delay(record)

    def perform_destroy(self, instance):
        destroyprocedurerecord.delay(instance)

    def perform_update(self, serializer):
        serializer.validated_data["update_time"] = datetime.now()
        serializer.save()

    def get_serializer_class(self):
        # if self.action == 'list':
        #     return SalaryRecordSerializer
        # else:
        #     return SalaryRecordSerializer
        return AppraisalProcedureSerializer
    def get_queryset(self):
        return AppraisalProcedure.objects.all()
    def get_permissions(self):
        return [IsSuperUser(),]


class EvaluateViewset(viewsets.ModelViewSet):
    """
    年度测评
    """
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = EvaluateSerializer
    pagination_class = Pagination

    def perform_create(self, serializer):
        record = serializer.save()
        createevaluateresult.delay(record)
    #
    # def perform_destroy(self, instance):
    #     destroyprocedurerecord.delay(instance)

    def perform_update(self, serializer):
        serializer.validated_data["update_time"] = datetime.now()
        serializer.save()

    def get_serializer_class(self):
        # if self.action == 'list':
        #     return SalaryRecordSerializer
        # else:
        #     return SalaryRecordSerializer
        return EvaluateSerializer
    def get_queryset(self):
        return Evaluate.objects.all()
    def get_permissions(self):
        return [IsSuperUser(),]
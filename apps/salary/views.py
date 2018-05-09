from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions
from .serializers import SalaryRecordSerializer,FSlarySerializer
from rest_framework.pagination import PageNumberPagination
from .models import SalaryRecord,FSalary
from django.contrib.auth import get_user_model
User = get_user_model()
from .task import createsalaryrecord,destroysalaryrecord
from datetime import datetime
from utils.permissions import IsSuperUser

class FSalaryPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100


class SalaryRecordViewset(viewsets.ModelViewSet):
    """
    工资记录操作
    """
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = SalaryRecordSerializer
    pagination_class = FSalaryPagination
    #lookup_field = "goods_id"

    def perform_create(self, serializer):
        salaryrecord = serializer.save()
        createsalaryrecord.delay(salaryrecord)
    #重写此方法则使用celery的删除， 否则自动级联删除
    def perform_destroy(self, instance):
        destroysalaryrecord.delay(instance)

    def perform_update(self, serializer):
        serializer.validated_data["update_time"] = datetime.now()
        serializer.save()



    def get_serializer_class(self):
        # if self.action == 'list':
        #     return SalaryRecordSerializer
        # else:
        #     return SalaryRecordSerializer
        return SalaryRecordSerializer
    def get_queryset(self):
        return SalaryRecord.objects.filter(user=self.request.user)

    def get_permissions(self):
        return [IsSuperUser(),permissions.IsAdminUser()]
        # if self.action == "retrieve":
        #     return [permissions.IsAuthenticated()]
        # elif self.action == "create":
        #     return [permissions.IsAdminUser()]
        # elif self.action == "list":
        #     return [permissions.IsAuthenticated()]
        # elif self.action == "update":
        #     return [permissions.IsAdminUser()]
        # elif self.action == "partial_update":
        #     return [permissions.IsAdminUser()]
        # elif self.action == "destroy":
        #     return [permissions.IsAdminUser()]
        # else:
        #     return [permissions.IsAuthenticatedOrReadOnly()]




class FSalaryViewset(viewsets.ModelViewSet):
    """
    薪酬明细
    """
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = FSlarySerializer
    pagination_class = FSalaryPagination
    def get_queryset(self):
        #return FSalary.objects.filter(user=self.request.user)
        if self.request.user.is_superuser:
            return FSalary.objects.all()
        elif self.request.user.is_staff:
            userdepart = self.request.user.user_depart.depart
            users = User.objects.filter(user_depart__depart=userdepart)
            return FSalary.objects.filter(user__in=users)
        else:
            return FSalary.objects.filter(user=self.request.user)
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return [IsSuperUser()]
        elif self.action == "list":
            return [permissions.IsAuthenticated()]
        elif self.action == "update":
            return [IsSuperUser(),permissions.IsAdminUser()]
        elif self.action == "partial_update":
            return [IsSuperUser(),permissions.IsAdminUser()]
        elif self.action == "destroy":
            return [IsSuperUser()]
        else:
            return [permissions.IsAuthenticated()]
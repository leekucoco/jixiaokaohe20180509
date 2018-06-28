from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions
from .serializers import SalaryRecordSerializer,FSlarySerializer
from rest_framework.pagination import PageNumberPagination
from .models import SalaryRecord,FSalary
from django.contrib.auth import get_user_model
User = get_user_model()
from .task import createsalaryrecord,destroysalaryrecord,sendmsg
from datetime import datetime
from utils.permissions import IsSuperUser
from rest_framework import filters
from django_filters import rest_framework as drffilters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.shortcuts import redirect
import time,json
from  decimal import Decimal
from rest_framework.response import Response
class FSalaryPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100



class FSalaryRecordFilter(drffilters.FilterSet):

    add_time = drffilters.DateTimeFromToRangeFilter()
    class Meta:
        model = SalaryRecord
        fields = ['status','user__username','add_time']

class SalaryRecordViewset(viewsets.ModelViewSet):
    """
    工资记录操作
    """
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = SalaryRecordSerializer
    pagination_class = FSalaryPagination
    #lookup_field = "goods_id"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = FSalaryRecordFilter
    #search_fields = ('user__name','user__idcardnumber','rank13demands__post__name',)
    ordering_fields = ('add_time','update_time')

    def perform_create(self, serializer):
        salaryrecord = serializer.save()
        createsalaryrecord.delay(salaryrecord)
    #重写此方法则使用celery的删除， 否则自动级联删除
    def perform_destroy(self, instance):
        destroysalaryrecord.delay(instance)

    def perform_update(self, serializer):
        #print(serializer.validated_data["checkonworkfile"])
        #print(serializer.validated_data["status"])
        serializer.validated_data["update_time"] = datetime.now()
        serializer.save()

        status = serializer.validated_data["status"]
        if status == "SENDMSG":
            sendmsg.delay(serializer.instance.id)
        else:
            pass




    def get_serializer_class(self):
        # if self.action == 'list':
        #     return SalaryRecordSerializer
        # else:
        #     return SalaryRecordSerializer
        return SalaryRecordSerializer
    def get_queryset(self):
        return SalaryRecord.objects.filter(user=self.request.user).order_by("-add_time")

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




class FSalaryFilter(drffilters.FilterSet):

    add_time = drffilters.DateTimeFromToRangeFilter()
    class Meta:
        model = FSalary
        fields = ['idcardnumber', 'srecord__id','user__username','add_time']



class FSalaryViewset(viewsets.ModelViewSet):
    """
    薪酬明细
    """
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = FSlarySerializer
    pagination_class = FSalaryPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = FSalaryFilter
    #search_fields = ('user__name','user__idcardnumber','rank13demands__post__name',)
    ordering_fields = ('add_time','update_time')
    def get_queryset(self):
        #return FSalary.objects.filter(user=self.request.user)
        if self.request.user.is_superuser:
            return FSalary.objects.all().order_by("-add_time")
        elif self.request.user.is_staff:
            userdepart = self.request.user.user_depart.depart
            users = User.objects.filter(user_depart__depart=userdepart)
            return FSalary.objects.filter(user__in=users).order_by("-add_time")
        else:
            return FSalary.objects.filter(user=self.request.user).order_by("-add_time")
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



class FSalaryRecordDataView(APIView):
    """
    修改个人工资记录的具体值，包括管理员的各种操作，上传请假记录等等
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsSuperUser,)

    def get(self, request):
        """
        处理工资表上传数据get
        """
        return Response("success")

    def post(self, request):
        """
        处理工资表上传数据post

        """
        resdata = {}
        successcount = 0
        errcount = 0
        data = request.data
        id = data.pop("id",None)
        jsboj = data.pop("jsonobj",None)
        status = data.pop("status",None)
        #print(id, jsboj,status)
        if status == "CHECKONWORKATTENDANCECOMPLETE":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__username = r["username"] )
                    if fs:
                        fsobj = fs[0]
                        privateaffairleavedays = int(r["privateaffairleavedays"])
                        sickleavedays = int(r["sickleavedays"])
                        basesalarythismonth = fsobj.basesalarythismonth
                        fsobj.privateaffairleavedays = privateaffairleavedays
                        fsobj.sickleavedays = sickleavedays
                        fsobj.basesalarythismonthwithleaves = basesalarythismonth/Decimal(21.75)*privateaffairleavedays+basesalarythismonth/Decimal(21.75)*sickleavedays/Decimal(2)
                        fsobj.save()
                        successcount = successcount + 1
                    else:
                        pass
                except Exception as e:
                    resdata[r["username"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "TOTALSALARYCOMPLETE":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__username = r["username"] )
                    if fs:
                        fsobj = fs[0]
                        basesalaryadd = Decimal(r["basesalaryadd"])
                        welfareresultadd = Decimal(r["welfareresultadd"])
                        fsobj.basesalaryadd = basesalaryadd
                        fsobj.welfareresultadd = welfareresultadd
                        fsobj.save()
                        successcount = successcount + 1
                    else:
                        pass
                except Exception as e:
                    resdata[r["username"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "INSURANCEANDFUNDCOMPELTE":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__username = r["username"] )
                    if fs:
                        fsobj = fs[0]
                        endowmentinsurance = Decimal(r["endowmentinsurance"])
                        medicalinsurance = Decimal(r["medicalinsurance"])
                        unemploymentinsurance = Decimal(r["unemploymentinsurance"])
                        housingprovidentfund = Decimal(r["housingprovidentfund"])
                        companyfund = Decimal(r["companyfund"])
                        totlainsuranceandfund = Decimal(r["totlainsuranceandfund"])
                        fsobj.endowmentinsurance = endowmentinsurance
                        fsobj.medicalinsurance = medicalinsurance
                        fsobj.unemploymentinsurance = unemploymentinsurance
                        fsobj.housingprovidentfund = housingprovidentfund
                        fsobj.companyfund = companyfund
                        fsobj.totlainsuranceandfund = totlainsuranceandfund
                        fsobj.save()
                        successcount = successcount + 1
                    else:
                        pass
                except Exception as e:
                    resdata[r["username"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "TAXANDOTHERDEDUCTIONS":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__username = r["username"] )
                    if fs:
                        fsobj = fs[0]
                        personaltax = Decimal(r["personaltax"])
                        partymemberdues = Decimal(r["partymemberdues"])
                        otherdeductions = Decimal(r["otherdeductions"])
                        fsobj.personaltax = personaltax
                        fsobj.partymemberdues = partymemberdues
                        fsobj.otherdeductions = otherdeductions
                        fsobj.save()
                        successcount = successcount + 1
                    else:
                        pass
                except Exception as e:
                    resdata[r["username"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "LOCK":
            pass
        elif status == "SENDMSG":
            pass
        else:
            return Response("无法确认上传数据处理程序")
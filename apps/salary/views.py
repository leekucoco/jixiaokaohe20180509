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

    def getcheckedvalue(self,key,klist,dobj):
        checkdata = lambda temp: temp if temp != "" else 0
        if key in klist:
            valres = checkdata(dobj[key])
        else:
            valres = "0.00"
        return valres

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
        faillist = []
        if status == "CHECKONWORKATTENDANCECOMPLETE":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__idcardnumber = r["身份证号"])
                    if fs:
                        fsobj = fs[0]
                        keyl = r.keys()
                        pdays = self.getcheckedvalue("事假天数",keyl,r)
                        sdays = self.getcheckedvalue("病假天数",keyl,r)
                        if Decimal(pdays) != 0 or Decimal(sdays) != 0:
                            privateaffairleavedays = Decimal(pdays)
                            sickleavedays = Decimal(sdays)
                            basesalarythismonth = fsobj.basesalarythismonth
                            fsobj.privateaffairleavedays = privateaffairleavedays
                            fsobj.sickleavedays = sickleavedays
                            fsobj.basesalarythismonthwithleaves = basesalarythismonth/Decimal(21.75)*privateaffairleavedays+basesalarythismonth/Decimal(21.75)*sickleavedays/Decimal(2)
                            fsobj.save()
                            successcount = successcount + 1
                            # print(successcount,fsobj.idcardnumber)
                        else:
                            pass
                    else:
                        faillist.append(r["身份证号"])
                except Exception as e:
                    resdata[r["身份证号"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            resdata["faildata"] = faillist
            resdata["failcount"] = len(faillist)
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "TOTALSALARYCOMPLETE":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__idcardnumber = r["身份证号"])
                    if fs:
                        fsobj = fs[0]
                        keyl = r.keys()
                        basesalaryaddtmp = self.getcheckedvalue("补发基本", keyl, r)
                        basesalaryadd = Decimal("".join(basesalaryaddtmp.split(",")))
                        welfareresultaddtmp = self.getcheckedvalue("补发福利", keyl, r)
                        welfareresultadd = Decimal("".join(welfareresultaddtmp.split(",")))
                        if basesalaryadd !=0 or welfareresultadd != 0:
                            fsobj.basesalaryadd = basesalaryadd
                            fsobj.welfareresultadd = welfareresultadd
                            fsobj.save()
                            successcount = successcount + 1
                        else:
                            pass
                    else:
                        faillist.append(r["身份证号"])
                except Exception as e:
                    resdata[r["身份证号"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            resdata["faildata"] = faillist
            resdata["failcount"] = len(faillist)
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "INSURANCEANDFUNDCOMPELTE":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__idcardnumber = r["身份证号"])
                    if fs:
                        fsobj = fs[0]
                        keyl = r.keys()
                        endowmentinsurancetmp = self.getcheckedvalue("养老保险", keyl, r)
                        # print(endowmentinsurancetmp)
                        endowmentinsurance = Decimal("".join(endowmentinsurancetmp.split(",")))
                        # print(endowmentinsurance)
                        medicalinsurancetmp = self.getcheckedvalue("医疗保险", keyl, r)
                        medicalinsurance = Decimal("".join(medicalinsurancetmp.split(",")))
                        unemploymentinsurancetmp = self.getcheckedvalue("失业保险", keyl, r)
                        unemploymentinsurance = Decimal("".join(unemploymentinsurancetmp.split(",")))
                        housingprovidentfundtmp = self.getcheckedvalue("住房公积金", keyl, r)
                        housingprovidentfund = Decimal("".join(housingprovidentfundtmp.split(",")))
                        companyfundtmp = self.getcheckedvalue("企业年金", keyl, r)
                        companyfund = Decimal("".join(companyfundtmp.split(",")))
                        totlainsuranceandfundtmp = self.getcheckedvalue("三险二金合计", keyl, r)
                        totlainsuranceandfund = Decimal("".join(totlainsuranceandfundtmp.split(",")))
                        if endowmentinsurance !=0 or medicalinsurance !=0 or unemploymentinsurance !=0\
                            or housingprovidentfund !=0 or companyfund !=0 or totlainsuranceandfund !=0:
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
                    else:
                        faillist.append(r["身份证号"])
                except Exception as e:
                    resdata[r["身份证号"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            resdata["faildata"] = faillist
            resdata["failcount"] = len(faillist)
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "TAXANDOTHERDEDUCTIONS":
            for r in jsboj:
                try:
                    fs = FSalary.objects.filter(srecord_id=id,user__idcardnumber = r["身份证号"])
                    if fs:
                        fsobj = fs[0]
                        keyl = r.keys()
                        personaltaxtmp = self.getcheckedvalue("个人所得税", keyl, r)
                        personaltax = Decimal("".join(personaltaxtmp.split(",")))
                        partymemberduestmp = self.getcheckedvalue("代缴党费", keyl, r)
                        partymemberdues = Decimal("".join(partymemberduestmp.split(",")))
                        otherdeductionstmp = self.getcheckedvalue("代扣其他", keyl, r)
                        otherdeductions = Decimal("".join(otherdeductionstmp.split(",")))
                        if personaltax != 0 or partymemberdues !=0 or otherdeductions !=0:
                            fsobj.personaltax = personaltax
                            fsobj.partymemberdues = partymemberdues
                            fsobj.otherdeductions = otherdeductions
                            fsobj.save()
                            successcount = successcount + 1
                        else:
                            pass
                            # print(r["身份证号"],r["姓名"],personaltax)
                    else:
                        faillist.append(r["身份证号"])
                except Exception as e:
                    resdata[r["身份证号"]] = str(e)
                    errcount = errcount + 1
            resdata["successcount"] = successcount
            resdata["errcount"] = errcount
            resdata["faildata"] = faillist
            resdata["failcount"] = len(faillist)
            json_str = json.dumps(resdata)
            return Response(json_str)
        elif status == "LOCK":
            pass
        elif status == "SENDMSG":
            pass
        else:
            return Response("无法确认上传数据处理程序")
import xadmin
from .models import SalaryRecord,FSalary
from django.contrib.auth import get_user_model
User = get_user_model()
class SalaryRecordAdmin(object):
    list_display = ["user","extrainfo","date", "checkonworkfile",
                    "baseandwelfareaddfile","insuranceandfundfile",
                    "taxandotherdeductionfile","status","add_time",]
    list_editable = ["extrainfo","date","checkonworkfile",
                    "baseandwelfareaddfile","insuranceandfundfile",
                    "taxandotherdeductionfile","status", ]
    search_fields = ['extrainfo', 'date', 'user__name','user__username', ]


    # def get_context(self):
    #     context = super(SalaryRecordAdmin, self).get_context()
    #     if 'form' in context:
    #         context['form'].fields['user'].queryset = SalaryRecord.objects.filter(user__id=1)
    #     return context

class FSalaryAdmin(object):
    list_display = ["user", "name", "srecord", "fltotal",
                    "ywslary","edslary","tislary","itslary",
                    "cmslary","basesalary", "basesalarythismonth",
                    "privateaffairleavedays","sickleavedays",
                    "basesalarythismonthwithleaves","basesalaryresult",
                    "welfareresult","basesalaryadd","welfareresultadd",
                    "totalsalaryresult","endowmentinsurance",
                    "medicalinsurance","unemploymentinsurance",
                    "housingprovidentfund","companyfund","totlainsuranceandfund",
                    "totalpayamount","personaltax","partymemberdues",
                    "otherdeductions","finalpayingamount","add_time",]
    #list_editable = ["name", ]
    #list_export = ('xls', 'json',)
    search_fields = ['name','user__username','srecord__extrainfo',]
    list_filter = ['name', 'add_time',]


    def queryset(self):
        qs = super(FSalaryAdmin, self).queryset()

        if self.request.user.is_superuser:

            return qs

        elif self.request.user.is_staff:
            userdepart = self.request.user.user_depart.depart
            users = User.objects.filter(user_depart__depart=userdepart)
            qs = qs.filter(user__in=users)
            return qs
        else:
            return qs

xadmin.site.register(SalaryRecord, SalaryRecordAdmin)
xadmin.site.register(FSalary, FSalaryAdmin)


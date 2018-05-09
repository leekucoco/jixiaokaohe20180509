import xadmin
from .models import AppraisalProcedure,AppraisalTicket,Evaluate,EvaluateResult
from django.contrib.auth import get_user_model
User = get_user_model()
class EvaluateAdmin(object):
    list_display = ["name","state","add_time","update_time",]
    list_editable = ["state", ]
    search_fields = ['name', 'state',]
    list_filter = ['name', 'add_time',]

class AppraisalProcedureAdmin(object):
    list_display = ["name","evaluateoftheyear","appraisalchoices","add_time","update_time",]
    search_fields = ['name','appraisalchoices','evaluateoftheyear__name',]
    list_filter = ['name', 'add_time',]

class AppraisalTicketAdmin(object):
    list_display = ["appraisalprocedure", "evaluateperson", "appraisedperson",
                    "score", "qualifications","add_time","update_time", ]
    search_fields = ['appraisalprocedure__name', 'evaluateperson__name', 'appraisedperson__name', ]
    list_filter = ['evaluateperson__name', 'add_time',"appraisedperson__name","appraisalprocedure", ]

class EvaluateResultAdmin(object):
    list_display = ["user","evaluateoftheyear", "ceoscore", "departleaderscore",
                    "bankleadersocre", "ceoresult", "departleaderesult", "bankleaderresult",
                    "qualificationsscore","democraticappraisalscore","leaderevaluatescore",
                    "qualifications","democraticappraisal","leaderevaluate","add_time","update_time",]
    search_fields = ['user__name',]
    list_filter = ['user__name','user__username', 'add_time', "update_time", "evaluateoftheyear", ]

    # def queryset(self):
    #     qs = super(FSalaryAdmin, self).queryset()
    #     if self.request.user.is_superuser:
    #         return qs
    #     elif self.request.user.is_staff:
    #         userdepart = self.request.user.user_depart.depart
    #         users = User.objects.filter(user_depart__depart=userdepart)
    #         qs = qs.filter(user__in=users)
    #         return qs
    #     else:
    #         return qs


xadmin.site.register(Evaluate, EvaluateAdmin)
xadmin.site.register(AppraisalProcedure, AppraisalProcedureAdmin)
xadmin.site.register(AppraisalTicket, AppraisalTicketAdmin)
xadmin.site.register(EvaluateResult, EvaluateResultAdmin)


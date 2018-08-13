import xadmin
from .models import SplitLevel,IndexPostLevel,\
    SplitMethod,PerformanceRecord,Quota,BankQuotaComplete,BankUploadRecord,BankUploadRecordDetail

class SplitLevelAdmin(object):
    list_display = ["name", 'desc',"add_time"]

class IndexPostLevelAdmin(object):
    list_display = ["post", "splitlevel"]

# class SplitMethodAdmin(object):
#     list_display = ["agent", "post","rank","demandyears","educationdemands",
#                     "primccbpdemands","titledemands","add_time",]
#     list_editable = ["rank","demandyears","educationdemands",
#                     "primccbpdemands","titledemands",]
#     search_fields = ['agent__name','post__name','rank', ]
# class Rank13CoefficentAdmin(object):
#     list_display = ["agent", "post","rank","level","coefficent","add_time",]
#     list_editable = ["coefficent", ]
#     search_fields = ['agent__name', 'post__name', 'coefficent',]

xadmin.site.register(SplitLevel, SplitLevelAdmin)
xadmin.site.register(IndexPostLevel, IndexPostLevelAdmin)
# xadmin.site.register(SplitMethod, SplitMethodAdmin)
# xadmin.site.register(Rank13Coefficent, Rank13CoefficentAdmin)


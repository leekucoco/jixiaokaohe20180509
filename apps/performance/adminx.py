import xadmin
from .models import SplitLevel,IndexPostLevel,\
    SplitMethod,PerformanceRecord,Quota,BankQuotaComplete,BankUploadRecord,BankUploadRecordDetail

class SplitLevelAdmin(object):
    list_display = ["name", 'desc',"add_time"]

class IndexPostLevelAdmin(object):
    list_display = ["kind","post", "splitlevel"]

class SplitMethodAdmin(object):
    list_display = ["info", "totalmoney","linguimenberstotalmoney","custmorsertotalmoney","accountingsupervisor",
                    "vpointernal","clerk","custmorsermanager","vpofield","creditgeneral","president","add_time"]
    list_editable = ["totalmoney","linguimenberstotalmoney","custmorsertotalmoney","accountingsupervisor",
                    "vpointernal","clerk","custmorsermanager","vpofield","creditgeneral","president"]
    search_fields = ['info' ]
    list_filter = ['info', 'add_time']

class PerformanceRecordAdmin(object):
    list_display = ["info", "splitmethod","state","add_time"]
    list_editable = ["info","state", "splitmethod"]
    search_fields = ['info',"state", 'splitmethod_info']
    list_filter = ['info',"state", 'add_time',"splitmethod"]

class QuotaAdmin(object):
    list_display = ["name", "desc","add_time"]
    list_editable = ["name", "desc","add_time"]
    search_fields = ["name", "desc","add_time"]
    list_filter = ["name", "desc","add_time"]

class BankQuotaCompleteAdmin(object):
    list_display = ["performancerecord", "depart","quota","plan","complete","add_time"]
    list_editable = ["performancerecord", "depart","quota","plan","complete","add_time"]
    search_fields = ['performancerecord', 'depart']
    list_filter = ['performancerecord', 'add_time',"depart"]


class BankUploadRecordAdmin(object):
    list_display = ["performancerecord","depart", "state","add_time"]
    list_editable = ["performancerecord","depart", "state","add_time"]
    search_fields = ["performancerecord","depart", "state","add_time"]
    list_filter = ['performancerecord', "depart", "state",'add_time']

class BankUploadRecordDetailAdmin(object):
    list_display = ["burecord", "user","quota","plan","complete","score","add_time"]
    list_editable = ["burecord", "user","quota","plan","complete","score","add_time"]
    search_fields = ["burecord", "user","quota","plan","complete","score","add_time"]
    list_filter = ["burecord", "user__name","quota","add_time"]

xadmin.site.register(SplitLevel, SplitLevelAdmin)
xadmin.site.register(IndexPostLevel, IndexPostLevelAdmin)
xadmin.site.register(SplitMethod, SplitMethodAdmin)
xadmin.site.register(PerformanceRecord, PerformanceRecordAdmin)
xadmin.site.register(Quota, QuotaAdmin)
xadmin.site.register(BankQuotaComplete, BankQuotaCompleteAdmin)
xadmin.site.register(BankUploadRecord, BankUploadRecordAdmin)
xadmin.site.register(BankUploadRecordDetail, BankUploadRecordDetailAdmin)

import xadmin
from xadmin import views
from .models import DepartDetail,IndexUserDepart

class DepartAdmin(object):
    list_display = ["agent","name", "dept_type", "parent_dept","manager","leader","basesalary",]
    list_editable = ["dept_type","parent_dept","manager","leader","basesalary",]
    list_filter = ["agent","name","dept_type","leader","basesalary",]
    search_fields = ["name","agent__name",]
class DepartUserAdmin(object):
    list_display = ["user","depart","add_time",]
    search_fields = ["user__name","depart__name","depart__agent__name","user__username"]


xadmin.site.register(IndexUserDepart, DepartUserAdmin)
xadmin.site.register(DepartDetail, DepartAdmin)
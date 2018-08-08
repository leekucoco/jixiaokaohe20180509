
import xadmin
from xadmin import views
from .models import CoefficientDetail

class CoefficientDetailAdmin(object):
    list_display = ["user","rank13demands","rank13coefficent", "coefficent", "is_special",
                    "addbasesalary","is_specialaddbasesalary","is_suspandwelfaresalary",
                    "basesalary","is_sepcialbasesalary"]
    search_fields =["user__name", "rank13demands__post__name","rank13demands__rank","user__username"]
    list_editable =["coefficent","addbasesalary","is_special","is_specialaddbasesalary",
                    "is_suspandwelfaresalary","basesalary","is_sepcialbasesalary"]
    list_filter = ['rank13demands', 'user__groups', ]

xadmin.site.register(CoefficientDetail, CoefficientDetailAdmin)

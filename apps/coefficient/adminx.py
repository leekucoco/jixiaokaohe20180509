
import xadmin
from xadmin import views
from .models import CoefficientDetail

class CoefficientDetailAdmin(object):
    list_display = ["user","rank13demands","rank13coefficent", "coefficent", "is_special","addbasesalary","is_specialaddbasesalary"]
    search_fields =["user__name", "rank13demands__post__name","rank13demands__rank"]
    list_editable =["coefficent","addbasesalary","is_special","is_specialaddbasesalary"]

xadmin.site.register(CoefficientDetail, CoefficientDetailAdmin)

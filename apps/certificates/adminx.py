
import xadmin
from xadmin import views
from .models import Cerficates, IndexUserCertificate

class CertificatesAdmin(object):
    list_display = ["name", "desc", "score","add_time",]
    search_fields =["name", "score",]
    list_editable =["name","score",]
    #style_fields = {"desc": "ueditor"}
class IndexUserCertificateAdmin(object):
    list_display = [ "user","certificate","image","add_time","update_time"]
    search_fields =["user__name","user__username", "certificate__name",]
    #list_editable =["certificate", "image",]

xadmin.site.register(Cerficates, CertificatesAdmin)
xadmin.site.register(IndexUserCertificate, IndexUserCertificateAdmin)
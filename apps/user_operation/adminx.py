
import xadmin
from .models import UserUploadBaseFiles


class UserUploadFilesAdmin(object):
    list_display = ["user","filename","message","file","add_time",]
    list_editable = ["user","filename","message","file",]
    search_fields = ["user__name","user__username","filename","message",]


xadmin.site.register(UserUploadBaseFiles, UserUploadFilesAdmin)

import xadmin
from xadmin import views
from .models import UserProfile
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "薪酬管理后台"
    site_footer = "DQRCBANK"
    # menu_style = "accordion"


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

class UserProfileAdmin(object):               # 自定义用户信息数据表管理器类
    # 设置xadmin后台显示字段
    list_display = ['username', 'idcardnumber', 'name', 'gender', 'email', 'mobile',
                    'joinedyears', 'workingyears', 'education', 'title','groups','is_staff']
    # 设置xadmin后台搜索字段，注意：搜索字段如果有时间类型会报错
    search_fields = ['username', 'idcardnumber', 'name', 'mobile']
    # 设置xadmin后台过滤器帅选字段，时间用过滤器来做
    list_filter = ['username','joinedyears']
    # model_icon = 'fa fa-user-plus'
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)

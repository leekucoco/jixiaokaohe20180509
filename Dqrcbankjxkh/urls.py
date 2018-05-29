from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from Dqrcbankjxkh.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

# from goods.views import GoodsListViewSet, CategoryViewset, HotSearchsViewset, BannerViewset
# from goods.views import IndexCategoryViewset
from users.views import  UserViewset
from user_operation.views import UploadFileViewset
# from trade.views import ShoppingCartViewset, OrderViewset
from depart.views import DepartViewset,IndexUserDeparViewset
from coefficient.views import CoefficientDetailViewset
from certificates.views import CerficatesViewset,IndexUserCertificateViewset
from rank13.views import Rank13CoefficentViewset,AgentViewset,PostViewset,Rank13DemandsViewset
from salary.views import SalaryRecordViewset,FSalaryViewset
from evaluate.views import AppraisalProcedureViewset,AppraisalTicketViewset,EvaluateResultViewset,EvaluateViewset

router = DefaultRouter()
router.register(r'evaluate', EvaluateViewset, base_name="evaluate")
router.register(r'appraisaprocedure', AppraisalProcedureViewset, base_name="appraisaprocedure")
router.register(r'appraisaticket', AppraisalTicketViewset, base_name="appraisaticket")
router.register(r'evaluateresult', EvaluateResultViewset, base_name="evaluateresult")
router.register(r'fsalary', FSalaryViewset, base_name="fsalary")
router.register(r'salaryrecord', SalaryRecordViewset, base_name="salaryrecord")
router.register(r'rank13coefficent', Rank13CoefficentViewset, base_name="rank13coefficent")
router.register(r'rank13demands', Rank13DemandsViewset, base_name="rank13demands")
router.register(r'agent', AgentViewset, base_name="agent")
router.register(r'post', PostViewset, base_name="post")
#配置goods的url
# router.register(r'goods', GoodsListViewSet, base_name="goods")

#配置category的url
# router.register(r'categorys', CategoryViewset, base_name="categorys")

router.register(r'depart', DepartViewset, base_name="depart")
router.register(r'indexdepartuser', IndexUserDeparViewset, base_name="indexdepartuser")
# router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

router.register(r'users', UserViewset, base_name="users")
router.register(r'certificate', CerficatesViewset, base_name="certificate")
router.register(r'indexusercertificate', IndexUserCertificateViewset, base_name="indexusercertificate")
router.register(r'cofficient', CoefficientDetailViewset, base_name="cofficient")
# #收藏
# router.register(r'userfavs', UserFavViewset, base_name="userfavs")
#
# #留言
# router.register(r'messages', LeavingMessageViewset, base_name="messages")
#
# #文件上传
router.register(r'uploadbasefile', UploadFileViewset, base_name="uploadbasefile")
#
# #收货地址
# router.register(r'address', AddressViewset, base_name="address")
#
# #购物车url
# router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")
#
# #订单相关url
# router.register(r'orders', OrderViewset, base_name="orders")
#
# #轮播图url
# router.register(r'banners', BannerViewset, base_name="banners")
#
# #首页商品系列数据
# router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")
#
#
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

# from trade.views import AlipayView
from django.views.generic import TemplateView
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^api/', include(router.urls)),

    # url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
    #
    # url(r'^laylogin/', TemplateView.as_view(template_name="laylogin.html"), name="laylogin"),
    # url(r'^layindex2/', TemplateView.as_view(template_name="layindex2.html"), name="layindex2"),
    # url(r'^laybackground/', TemplateView.as_view(template_name="laybackground.html"), name="layindex"),
    url(r'docs/', include_docs_urls(title="后台管理")),

    #drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    # url(r'^alipay/return/', AlipayView.as_view(), name="alipay"),
]



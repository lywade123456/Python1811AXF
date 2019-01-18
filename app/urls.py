from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^home/$', views.home, name='home'),   # 首页
    url(r'^market/(\d+)/(\d+)/$', views.market, name='market'), # 闪购超市
    url(r'^cart/$', views.cart, name='cart'),   # 购物车
    url(r'^mine/$', views.mine, name='mine'),   # 我的

    url(r'^login/$', views.login, name='login'),    # 登录
    url(r'^register/$', views.register, name='register'),   # 注册
    url(r'^checkemail/$', views.checkemail, name='checkemail'), # 验证邮箱
    url(r'^logout/$', views.logout, name='logout'), # 退出

    url(r'^addcart/$', views.addcart, name='addcart'), # 加操作
    url(r'^subcart/$', views.subcart, name='subcart'),  # 减操作
    url(r'^changecartstatus/$', views.changecartstatus, name='changecartstatus'),   # 修改购物车记录选中状态
    url(r'^changecartall/$', views.changecartall, name='changecartall'),    # 全选操作


    url(r'^generateorder/$', views.generateorder, name='generateorder'),    # 下单
    url(r'^orderlist/(\d+)/$', views.orderlist, name='orderlist'),
    url(r'^orderdetail/(.+)/$', views.orderdetail, name='orderdetail'),    #　订单详情
    url(r'^pay/$', views.pay, name='pay'),  # 支付
    url(r'^appnotify/$', views.appnotify, name='appnotify'),    # 支付完成后(服务器)
    url(r'^returnview/$', views.returnview, name='returnview'), # 买家支付完成后回到AXF哪个页面(客户端)
]

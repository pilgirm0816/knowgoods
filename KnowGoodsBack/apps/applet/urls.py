from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('pay',views.PayViewSet,'pay')
router.register('orderlist',views.Order_listViewSet,'orderlist')

urlpatterns = [
    path('get_code/', views.Get_code.as_view()),
    path('home/navbars/', views.Rt_navbars.as_view()),
    path('home/banners/', views.Rt_banners.as_view()),
    path('home/productsale/', views.Rt_productsale.as_view()),
    path('home/pecialbenefits/', views.Rt_pecialbenefits.as_view()),
    path('gooddetail/', views.Rt_gooddetail.as_view({'get': 'retrieve'})),
    path('category/', views.Rt_category.as_view()),
    path('category/index/', views.Rt_categoryindex.as_view({'get': 'list'})),
    path('category/preview/', views.Rt_categorypreview.as_view({'get': 'list'})),
    path('login/', views.Get_userdetail.as_view()),
    path('mine/address/', views.Save_address.as_view()),
    path('addcartgood/', views.AddCartGoodView.as_view()),
    path('delcartgood/', views.DelCartGoodView.as_view()),
    path('order/success/', views.Post_Pay_success),
    path('pay/success/', views.Get_Pay_success),

]

urlpatterns += router.urls

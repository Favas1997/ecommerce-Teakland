
from django.urls import path
from . import views

urlpatterns = [
    path("",views.login,name="login1"),
    path("home/",views.home,name="home"),
    path("user/",views.user,name="user"),
    path("addproducts/",views.addproducts,name="addproducts"),
    path("viewproducts/",views.viewproducts,name="viewproducts"),
    path("product_delete/<int:id>/",views.product_delete,name="product_delete"),
    path("product_edit/<int:id>/",views.product_edit,name="product_edit"),
    path("viewcategory/",views.viewcategory,name="viewcategory"),
    path("category_delete/<int:id>/",views.category_delete,name='category_delete'),
    path("addcategory/",views.addcategory,name='addcategory'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('block/<int:id>/',views.block,name='block'),
    path('logout/',views.logout,name='logout'),
    path('order_list/',views.order_list,name='order_list'),
    path('order_status/',views.order_status,name='order_status'),
    path('report_search/',views.report_search,name='report_search'),
    path('addoffer/<int:id>/',views.addoffer,name='addoffer'),
    path('deleteoffer/<int:id>/',views.deleteoffer,name='deleteoffer'),
    path('view_coupon/',views.view_coupon,name='view_coupon'),
    path('delete_coupon/<int:id>/',views.delete_coupon,name='delete_coupon')
  

]    

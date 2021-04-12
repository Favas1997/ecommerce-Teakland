
from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path('login/',views.login, name="login"),
    path('register/',views.register, name='register'),
    path('logout/',views.logout, name='userlogout'),
    path('product_details/<int:id>/',views.product_details,name='product_details'),
    path('product_categ/<int:id>/',views.product_categ,name='product_categ'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart_count/',views.cart_count,name='cart_count'),
    path('cart_delete/<int:id>/',views.cart_delete,name='cart_delete'),
    path('checkout/',views.checkout,name='checkout'),
    path('add_address/',views.add_address,name='add_address'),
    path('select_address/<int:id>/',views.select_address,name='select_address'),
    path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
    path('payment_method/',views.payment_method,name='payment_method'),
    path('cod/',views.cod,name='cod'),
    path('paypal/',views.paypal,name='paypal'),
    path('paypal_success/',views.paypal_success,name='paypal_success'),
    path('razorpay/',views.razorpay,name='razorpay'),
    path('my_account/',views.my_account,name='my_account'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('edit_details/',views.edit_details,name='edit_details'),
    path('otp_request/',views.otp_requset,name='otp_request'),
    path('otp_validate/',views.otp_validate,name='otp_validate'),
    path('addimage/',views.addimage,name='addimage'),
    path('search/',views.search,name='search'),
    path('cancel_order/<int:id>/',views.cancel_order,name='cancel_order'),
    path('referal/<int:id>/',views.referal_code,name='referal')


    
    

]    

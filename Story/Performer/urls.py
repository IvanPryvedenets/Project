from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='Home_page_url'),
    path('product/<str:slug>/', ProductInformation.as_view(), name='Product_information_url'),
    path('cart/', Cart.as_view(), name='Cart_url'),
    path('checkout/', Checkout.as_view(), name='Checkout_url'),
    path('checkout/successful_order/', successful_order, name='successful_order_url'),
    path('user_profile/', Profile.as_view(), name='User_profile_url'),
    path('login_user/', login_user, name='Login_user_url'),
    path('logout_user/', logout_user, name='Logout_user_url'),

    path('jqueryworker/', func, name='JqueryWorker')
]

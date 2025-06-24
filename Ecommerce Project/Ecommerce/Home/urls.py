from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.Home, name='home'),
    path('api/', views.api_views, name='api'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('newsletter/', views.newsletter, name='newsletter'),
    
    #payment razorpay urls make sure all the this enebled in settings.py and views
    # path('checkout/', views.initiate_payment, name='checkout'),
    # path('payment/callback/', views.payment_callback, name='payment_callback'),
    # path('order/success/', views.order_success, name='order_success'),
]
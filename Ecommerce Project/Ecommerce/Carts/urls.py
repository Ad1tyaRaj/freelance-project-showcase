from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('promocode/', views.apply_promocode, name='apply_promocode'),
    path('remove-promo/', views.remove_promo, name='remove_promo'),
    path('checkout/', views.checkout, name='checkout'),
    path('become_seller/', views.become_seller, name='become_seller'),
    path('seller_products/', views.seller_products, name='seller_products'),
    path('seller/add-product/', views.add_product, name='add_product'),
    path('seller/edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

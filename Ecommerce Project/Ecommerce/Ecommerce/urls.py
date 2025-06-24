from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Home import views as home_views
from Products import views as products_views
from Carts import views as carts_views

# API Router
router = DefaultRouter()
router.register(r'newsletter', home_views.NewsletterViewSet)
router.register(r'products', home_views.ProductsViewSet)
router.register(r'buy_items', home_views.Buy_itemsViewSet)
router.register(r'orders', home_views.Order_itemsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('products/', include('Products.urls')),
    path('accounts/', include('Accounts.urls')),
    path('cart/', include('Carts.urls')),

    # API URLs
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

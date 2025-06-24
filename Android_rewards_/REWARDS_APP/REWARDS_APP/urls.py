from django.contrib import admin
from django.urls import path, include
#API
from rest_framework.routers import DefaultRouter
from Home import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# API URLs
router = DefaultRouter()
router.register(r'apps', views.AndroidAppViewSet)
router.register(r'tasks', views.UserTaskViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    # API URLs
    path('get/', include(router.urls)),
    path('get/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# for Api -----------



schema_view = get_schema_view(
   openapi.Info(
      title="Task Submission API",
      default_version='v1',
      description="API documentation for the Task Submission Platform",
      contact=openapi.Contact(email="code.adityaraj@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
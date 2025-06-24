from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.Home, name='home'),
    path('api/', views.api_view, name='api'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dash/', views.admin_dash_view, name='admin-dash'),
    path('task/', views.task_view, name='task'),
    path('submit/', views.submit_view, name='submit_view'),
    path('admin_settings/', views.admin_setting, name='admin_settings'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('add_task/', views.add_task, name='add_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('logout/', views.logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


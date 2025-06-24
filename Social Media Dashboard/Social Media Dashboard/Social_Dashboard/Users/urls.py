from django.urls import path
from . import views



urlpatterns = [
    path('',views.Base,name= 'Base'),
    path('signup',views.Signup,name= 'signup'),
    path('login',views.Login,name= 'login'),
    path('profile',views.Profile,name='profile'),
    path('facebook',views.Facebook,name='facebook'),
    path('create_post',views.Create_post,name= 'create_post'),
    path('twitter',views.twitter,name='twitter'),
    path('create_twitter_post', views.Create_twitter_post, name='create_twitter_post'),
    path('instagram',views.instagram,name='instagram'),
    path('linkedin',views.linkedin,name='linkedin'),
    path('analytics',views.analytics,name='analytics'),
    path('schedule',views.schedule,name='schedule'),
    path('settings',views.settings,name='settings'),
    path('logout',views.logout,name='logout'),
]

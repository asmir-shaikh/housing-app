from django.urls import path

from . import views

app_name = 'oauth_app'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('submit/', views.HousingForm, name='HousingForm'),
    path('housing_detail/<int:housing_id>/', views.Housing_Detail, name='housing_detail'),
    path('housing_detail/popularity/<int:housing_id>/', views.popularity, name='popularity'),
    path('fav/<int:housing_id>/', views.fav_add, name='fav_add'),
    path('favorites/', views.favorites, name='favorites'),
    path('unofficial', views.unofficial, name='unofficial'),
    path('profile', views.profile, name='profile'),
]

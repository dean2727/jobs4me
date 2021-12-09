from django.urls import path

from . import views

app_name = 'jobs4me'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),

    path('admin_portal/', views.adminTest, name='admin-portal')
]
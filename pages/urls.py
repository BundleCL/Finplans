from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('results', views.results, name='results'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]

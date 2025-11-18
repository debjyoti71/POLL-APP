from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('polls/', views.poll_list, name='poll_list'),
    path('polls/<slug:slug>/', views.poll_detail, name='poll_detail'),

]

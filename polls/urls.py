from django.urls import path
from . import views, auth_views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Poll pages
    path('polls/', views.poll_list, name='poll_list'),
    path('polls/create/', views.create_poll, name='create_poll'),
    path('my-polls/', views.my_polls, name='my_polls'),
    path('polls/<slug:slug>/', views.poll_detail, name='poll_detail'),

    # Voting
    path('vote/<int:pk>/', views.vote, name='vote'),

    # Auth pages
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.user_login, name='login'),
    path('logout/', auth_views.user_logout, name='logout'),
]

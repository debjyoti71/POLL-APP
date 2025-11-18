from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Poll pages
    path('polls/', views.poll_list, name='poll_list'),
    path('polls/create/', views.create_poll, name='create_poll'),
    path('polls/<slug:slug>/', views.poll_detail, name='poll_detail'),

    # Voting
    path('vote/<int:pk>/', views.vote, name='vote'),

    # Auth pages
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
]

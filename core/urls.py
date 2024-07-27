from django.urls import path
from . import views

# URLconf
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('base/', views.base, name='base'),
    path('profile/', views.profile, name='profile'),
    path('quiz/', views.index, name='index'),
    path('quiz/<int:topic_id>/', views.quiz, name='quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]

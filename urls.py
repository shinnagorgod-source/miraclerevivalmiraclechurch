from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sermons/', views.sermons, name='sermons'),
    path('sermons/<int:pk>/', views.sermon_detail, name='sermon_detail'),
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('ministries/', views.ministries, name='ministries'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('prayer-request/', views.prayer_request, name='prayer_request'),
    path('give/', views.give, name='give'),
    path('videos/', views.videos, name='videos'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/<str:difficulty>/', views.quiz_play, name='quiz_play'),
]

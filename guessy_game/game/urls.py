from django.urls import path
from.views import index, play

urlpatterns = [
        path('', index, name='index'),
        path('play/', play, name='play'),
        ]

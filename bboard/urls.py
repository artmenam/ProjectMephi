from django.urls import path

from .views import index, predict1

urlpatterns = [
    path('index/', index),
    path('predict/',predict1)
]
from django.urls import path

from .views import index, predict1, stock

urlpatterns = [
    path('index/', index),
    path('prediction/',predict1),
    path('stocks/', stock),
]


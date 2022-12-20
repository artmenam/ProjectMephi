from django.urls import path

from .views import predict1, stock, allstock

urlpatterns = [
    path('prediction/<str:stockname>/', predict1),
    path('stocks/<str:stockname>/', stock),
    path('stocks/', allstock),
]


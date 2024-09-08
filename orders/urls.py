from django.contrib import admin
from django.urls import path, include
from project.settings import MEDIA_ROOT, MEDIA_URL
from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketPlaceViews 


urlpatterns = [
    path('placeOrder/', views.placeOrder,name="placeOrder"),
    path('payments/', views.payments,name="payments"),
    path('orderComplete/', views.orderComplete,name="orderComplete"),
   
] 
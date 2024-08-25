from django.urls import path
from . import views


urlpatterns = [
    path('', views.marketPlace, name='marketPlace'),
    path('<slug:vendor_slug>/', views.vendorDetail, name='vendorDetail'),
    path('removeItemFromCart/<int:foodId>/', views.removeItemFromCart, name='removeItemFromCart'),
    path('addItemToCart/<int:foodId>/', views.addItemToCart, name='addItemToCart'),
    path('deleteCartItem/<int:cartId>/', views.deleteCartItem, name='deleteCartItem'),
    
   
]
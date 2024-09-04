from django.urls import include, path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.customerDashboard, name='customerDashboard'),
    path('profile/', views.customerProfile, name='customerProfile'),
    
]
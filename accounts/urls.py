from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.myAccount),
    path('registerUser/',  views.registerUser, name='registerUser'),
    path('registerVendor/',  views.registerVendor, name='registerVendor'),
    path('login/',  views.login, name='login'),
    path('logout/',  views.logout, name='logout'),
    path('customerDashboard/',  views.customerDashboard, name='customerDashboard'),
    path('vendorDashboard/',  views.vendorDashboard, name='vendorDashboard'),
    path('myAccount/',  views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>/',  views.activate, name='activate'),
    path('forgotPassword/',  views.forgotPassword, name='forgotPassword'),
    path('resetPassword/',  views.resetPassword, name='resetPassword'),
    path('resetPassword/<uidb64>/<token>/',  views.resetPasswordValidation, name='resetPasswordValidation'),
    path('vendor/', include('vendors.urls')),
    path('customer/', include('customers.urls')),
]
from django.urls import path
from . import views
from accounts import views as accountViews

urlpatterns = [
    path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/',  views.vendorProfile, name='vendorProfile'),
    path('menuBuilder/',  views.menuBuilder, name='menuBuilder'),

    path('menuBuilder/category/<int:id>/',  views.foodItemsByCategory, name='foodItemsByCategory'),
    path('menuBuilder/category/add/',  views.addCategory, name='addCategory'),
    path('menuBuilder/editCategory/<int:id>/',  views.editCategory, name='editCategory'),
    path('menuBuilder/deleteCategory/<int:id>/',  views.deleteCategory, name='deleteCategory'),

    path('menuBuilder/addFoodItem/<int:id>/',  views.addFoodItem, name='addFoodItem'),
    path('menuBuilder/editFoodItem/<int:cid>/<int:fid>',  views.editFoodItem, name='editFoodItem'),
    path('menuBuilder/deleteFoodItem/<int:id>/',  views.deleteFoodItem, name='deleteFoodItem'),
    
    
]
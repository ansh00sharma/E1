from django import forms
from menu.models import Category, FoodItem
from accounts.validators import allowOnlyImagesValidator

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']


class AddFoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}),validators=[allowOnlyImagesValidator])
    class Meta:
        model = FoodItem
        fields = ['food_title','description','price','image','is_available']        
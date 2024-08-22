from django import forms
from menu.models import Category


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']
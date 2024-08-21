from django import forms
from vendors.models import Vendor
from .models import User
from accounts.forms import UserForm
from accounts.validators import allowOnlyImagesValidator

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}), validators=[allowOnlyImagesValidator])
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']

    # def clean(self):
    #     cleaned_data = super(UserForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')

    #     if password != confirm_password:
    #         raise forms.ValidationError("Password does not match !")    
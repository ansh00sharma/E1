import accounts.forms
from django import forms
import django.shortcuts
from .models import User, UserProfile
from .validators import allowOnlyImagesValidator

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match !")
        

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start Typing Address ...', 'required':'required'}),validators=[allowOnlyImagesValidator])
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allowOnlyImagesValidator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={"class":"btn btn-info"}), validators=[allowOnlyImagesValidator])
    
    # longitute = forms.CharField(widget=forms.TextInput(attrs={"readonly":"readonly"}))
    class Meta:
   
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','country','state','city','pincode','longitude','latitude']         

    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
               if field == 'longitude' or field == 'latitude':
                   self.fields[field].widget.attrs['readonly'] = 'readonly'
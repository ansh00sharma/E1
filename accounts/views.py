from django.shortcuts import render, redirect
from vendors.forms import VendorForm
from . forms import UserForm
from . models import User, UserProfile
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            user = User.objects.create_user(first_name,last_name,username=username,email=email,password=password)
            user.phone_number = phone_number
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered Successfully")
            return redirect('registerUser')
        else:
            pass
    else:
        form = UserForm()   

    context = {
        'form':form
    }
    return render(request, 'accounts/registerUser.html',context)


def registerVendor(request):
    if request.method == "POST":
        u_form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if v_form.is_valid() and u_form.is_valid():
            first_name = u_form.cleaned_data['first_name']
            last_name = u_form.cleaned_data['last_name']
            password = u_form.cleaned_data['password']
            email = u_form.cleaned_data['email']
            phone_number = u_form.cleaned_data['phone_number']
            username = u_form.cleaned_data['username']
            user = User.objects.create_user(first_name,last_name,username=username,email=email,password=password)
            user.phone_number = phone_number
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)    
            vendor.user = user
            vendor_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = vendor_profile
            vendor.save()

            messages.success(request, "Your account has been registered Successfully! Please wait for approval.")
            return redirect('registerVendor')
        else:
            pass
    else:
        u_form = UserForm()
        v_form = VendorForm()    

    context = {
        'u_form':u_form,
        'v_form':v_form
    }
    return render(request, 'accounts/registerVendor.html',context)
from django.shortcuts import render, redirect
from vendors.forms import VendorForm
from accounts.models import User
from accounts.utils import detectUser
from . forms import UserForm
from . models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    

# Main views    
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in to your Account !")
        return redirect('myAccount')
    
    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in to your Account !")
        return redirect('myAccount')
    
    elif request.method == "POST":
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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in to your Account !")
        return redirect('myAccount')
    
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,"You are Successfully logged in your Account.")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid Credentials")   
            return redirect('login') 
        
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You have Successfully logged out of your Account")
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)
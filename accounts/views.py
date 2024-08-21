import django.contrib.auth.tokens
from django.shortcuts import render, redirect
import django.utils.http
from vendors.forms import VendorForm
from accounts.models import User
from accounts.utils import detectUser , send_verification_email
from . forms import UserForm
from . models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendors.models import Vendor

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

            # Send verification email to user
            mail_subject = 'Please Activate Your Account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)

            messages.success(request, "Your account has been registered Successfully ! Please Activate it through your registered Email BEFORE loggin in.")
            return redirect('login')
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
 
             # Send verification email to Vendor
            mail_subject = 'Please Activate Your Account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)

            messages.success(request, "Your account has been registered Successfully! Please Activate it through your registered Email BEFORE loggin in.")
            return redirect('login')
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
    vendor = Vendor.objects.get(user = request.user)  
    context = {
        'vendor' : vendor
    }
    return render(request, 'accounts/vendorDashboard.html',context)

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    print(user)
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() 
        user = User._default_manager.get(pk=uid)
    except(TypeError, OverflowError,ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your Account is Activated.")
        return redirect(myAccount)    
    else:
        messages.success(request, "Invalid Activation Link.")
        return redirect(myAccount)
    
def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email) 

            # send reset password email           
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/resetPasswordEmail.html'
            send_verification_email(request,user,mail_subject,email_template)

            messages.success(request, "Link to Reset your Password has been send to Your Registered Email.")
            return redirect('login')
        else:
            messages.success(request, "Account with this Email is not registerd yet.")
            return redirect('forgotPassword')
        
    return render(request,'accounts/forgotPassword.html')   


def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.set_active = True
            user.save()
            messages.success(request, "Your Password has been reset Successfully !")
            return redirect('login')
        else:
            messages.error(request, "Passwords do Not match, Try Again.")
            return redirect(resetPassword)
        
    return render(request,'accounts/resetPassword.html')    


def resetPasswordValidation(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() 
        user = User._default_manager.get(pk=uid)
    except(TypeError, OverflowError,ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, "Please Reset your Password.")
        return redirect('resetPassword')
    else:
        messages.error(request, "The Link to reset Password has Expired !")
        return redirect('myAccount')




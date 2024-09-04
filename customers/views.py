from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.forms import UserProfileForm, CustomerInfoForm
from accounts.models import UserProfile
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def customerProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        p_form = UserProfileForm(request.POST, request.FILES,instance=profile)
        c_form = CustomerInfoForm(request.POST,instance=request.user)

        if p_form.is_valid() and c_form.is_valid():
            p_form.save()
            c_form.save()
            messages.success(request, "User Profile Updated Successfully !") 
            redirect('customerProfile')
        else:
            print(p_form.errors)
            print(c_form.errors)
    else:
        p_form = UserProfileForm(instance=profile)
        c_form = CustomerInfoForm(instance=request.user)
    context = {
        'p_form':p_form,
        'c_form':c_form,
        'profile':profile
    }
    return render(request, "customers/profile.html",context=context)
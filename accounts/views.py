from django.shortcuts import render, redirect
from . forms import UserForm
from . models import User
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


def registerRestaurant(request):
    return render(request, 'accounts/registerRestaurant.html')
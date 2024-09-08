from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.forms import UserProfileForm, CustomerInfoForm
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import Order, OrderedFood
import simplejson as json

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


def myOrder(request):
    order = Order.objects.filter(user=request.user, is_ordered=True).order_by("-created_at")
    context = {
        'orders':order,
    }
    return render(request, 'customers/myOrder.html',context=context)

def orderDetails(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': round(subtotal,2),
            'tax_data': tax_data,
        }
        return render(request, 'customers/orderDetails.html', context)
    except Exception as e:
        print(str(e))
        return redirect('customerDashboard')    
    
    
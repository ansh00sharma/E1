from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import UserProfile
from vendors.models import Vendor
from menu.apps import MenuConfig
from menu.models import Category, FoodItem
from menu.forms import AddCategoryForm
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from django.template.defaultfilters import slugify
# Create your views here.


def get_vendor(request):
    return Vendor.objects.get(user = request.user)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Your Restaurant Profile has been Updated !")
            return redirect("vendorProfile")
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'p_form' : profile_form,
        'v_form' : vendor_form,
        'profile' : profile,
        'vendor' : vendor
    }
    return render(request, 'vendors/vendorProfile.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories' : categories
    }  

    return render(request, 'vendors/menuBuilder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def foodItemsByCategory(request,id=None):
    vendor = get_vendor(request)
    categories = get_object_or_404(Category, pk=id)
    fooditems = FoodItem.objects.filter(vendor=vendor, category = categories)
    
    context = {
        'category':categories,
        'fooditems' : fooditems
    }
    return render(request, 'vendors/foodItemsByCategory.html',context)    

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def editCategory(request,id=None):
    categories = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        form = AddCategoryForm(request.POST, instance=categories)
        if form.is_valid():
            category_name = form.cleaned_data['category_name'] 
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category Updated Successfully !") 
            return redirect("menuBuilder")
    else:
        form = AddCategoryForm(instance=categories)
    context = {
        'form':form,
        'category':categories
    }
    return render(request, 'vendors/editCategory.html', context) 
      
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def deleteCategory(request,id=None):
    
    category = get_object_or_404(Category, pk=id)
    category.delete()
    messages.success(request, "Category Deleted Successfully !") 
    return redirect("menuBuilder")
    


def addCategory(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name'] 
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "New Category Added Successfully !") 
            return redirect("menuBuilder")
    else:
        form = AddCategoryForm()
    context = {
        'form':form
    }
    return render(request, "vendors/addCategory.html",context)    
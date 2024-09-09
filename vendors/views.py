from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse, HttpResponse
from accounts.models import UserProfile
from vendors.models import OpeningHour, Vendor
from menu.models import Category, FoodItem
from menu.forms import AddCategoryForm, AddFoodItemForm
from orders.models import Order, OrderedFood
from .forms import VendorForm, OpeningHourForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test 
from accounts.views import check_role_vendor
from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError
# Create your views here.


def get_vendor(request):
    return Vendor.objects.get(user = request.user)

def get_category(vendor,id):
    # return Category.objects.get(vendor = vendor, pk=id)
    return get_object_or_404(Category, pk=id)


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
        form = AddCategoryForm(request.POST, request.FILES, instance=categories)
        if form.is_valid():
            category_name = form.cleaned_data['category_name'] 
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            new_slug = str(category_name)+str(category.vendor)
            # category.slug = slugify(category_name)
            category.slug = slugify(new_slug)
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
    

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def addCategory(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name'] 
            category = form.save(commit=False)
                        
            category.vendor = get_vendor(request)
            new_slug = str(category_name)+str(category.vendor)
            # category.slug = slugify(category_name)
            category.slug = slugify(new_slug)
            form.save()
            messages.success(request, "New Category Added Successfully !") 
            return redirect("menuBuilder")
    else:
        form = AddCategoryForm()
    context = {
        'form':form
    }
    return render(request, "vendors/addCategory.html",context)    


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def addFoodItem(request, id=None):
    if request.method == "POST":
        form = AddFoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title'] 
            fooditem = form.save(commit=False)

            vendor = get_vendor(request)
            category = get_category(vendor,id)
            print(vendor, category)
            fooditem.vendor = vendor
            fooditem.category = category
            new_slug = str(vendor)+str(food_title)
            # fooditem.slug = slugify(food_title)
            fooditem.slug = slugify(new_slug)
            form.save()
            messages.success(request, "New Food Item Added Successfully !") 
            return redirect("foodItemsByCategory", fooditem.category.id)
    else:
        form = AddFoodItemForm()
    context = {
        'form':form,
        'cat_id' : id
    }
    return render(request, "vendors/addFoodItem.html",context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def editFoodItem(request, cid=None,fid=None):
    print(cid,fid)
    food_item = get_object_or_404(FoodItem, pk=fid)
    if request.method == "POST":
        form = AddFoodItemForm(request.POST, request.FILES,instance=food_item)
        if form.is_valid():
            food_title = form.cleaned_data['food_title'] 
            fooditem = form.save(commit=False)

            vendor = get_vendor(request)
            category = get_category(vendor,cid)

            fooditem.vendor = vendor
            fooditem.category = category
            
            new_slug = str(vendor)+str(food_title)
            # fooditem.slug = slugify(food_title)
            fooditem.slug = slugify(new_slug)
            form.save()
            messages.success(request, "Food Item  Updated Successfully !") 
            return redirect("foodItemsByCategory", fooditem.category.id)
    else:
        form = AddFoodItemForm(instance=food_item)
    context = {
        'form':form,
        'food':food_item,
        'cid' : cid
        
    }
    
    return render(request, "vendors/editFoodItem.html",context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def deleteFoodItem(request,id=None):

    fooditem = get_object_or_404(FoodItem, pk=id)
    fooditem.delete()
    messages.success(request, "Food Item Deleted Successfully !") 
    return redirect("foodItemsByCategory", fooditem.category.id)


def openingHour(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form':form,
        'opening_hours':opening_hours
    }
    return render(request, 'vendors/openingHour.html',context)


def addOpeningHour(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method=="POST":
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request),day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status':'success','id':hour.id,'day':day.get_day_display(),'is_closed':'Closed'}
                    else:
                        response = {'status':'success','id':hour.id,'day':day.get_day_display(),'from_hour':hour.from_hour,'to_hour':hour.to_hour}    
                
                return JsonResponse(response) 
            except IntegrityError as e:
                response = {'status':'failed','message':from_hour+'-'+to_hour+'  already exists for this day !'}
                return JsonResponse(response) 

        else:
            return HttpResponse("Invalid Request")



def removeOpeningHour(request,id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour,pk=id)
            hour.delete()
            print("deleted")
            return JsonResponse({'status':'success','id':id})

     
def orderDetails(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'sub_total': order.get_total_by_vendor()['subtotal'],
            'tax_dict': order.get_total_by_vendor()['tax_dict'],
            'grand_total':order.get_total_by_vendor()['grand_total']
        }
        return render(request,'vendors/orderDetails.html',context=context)
    except:
        return redirect('vendor')

def vendorMyOrders(request):
    vendor = Vendor.objects.get(user = request.user)  
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by("-created_at")
    context = {
        'vendor' : vendor,
        'orders':orders,
    }
    return render(request, 'vendors/vendorMyOrders.html', context=context)        
    
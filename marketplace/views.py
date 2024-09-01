from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch
from vendors.models import OpeningHour, Vendor
from menu.models import Category, FoodItem
from .models import Cart
from .contextProcessors import getCartCounter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
# Create your views here.

def marketPlace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count
    }
    return render(request, 'marketplace/listing.html',context)


def vendorDetail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug = vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems',queryset= FoodItem.objects.filter(is_available=True))
    )

    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','from_hour')
    today_opening_hours = OpeningHour.objects.filter(vendor=vendor,day=date.today().isoweekday())
    current_time = datetime.now().strftime("%H:%M:%S")

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user= request.user)
    else:
        cart_items = None    
    content = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
        'opening_hours':opening_hours,
        'today_opening_hours':today_opening_hours,
    }
    return render(request, 'marketplace/vendorDetail.html',content)


def addItemToCart(request,foodId):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=foodId)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': getCartCounter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': getCartCounter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

    


def removeItemFromCart(request,foodId):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=foodId)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': getCartCounter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this Food item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This Food Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})  

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items':cart_items
    }
    return render(request,'marketplace/cart.html',context)


@login_required(login_url='login')
def deleteCartItem(request,cartId):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_items  = Cart.objects.get(user=request.user,id=cartId)
                if cart_items:
                    cart_items.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been Deleted','cart_counter': getCartCounter(request),'cart_amount': get_cart_amounts(request)})  
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not Exist'})     
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})     
    return

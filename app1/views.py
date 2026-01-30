from django.shortcuts import render,redirect,get_object_or_404
from .forms import CustomUserCreationForm,EmailLoginForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import Product,Cart,Order
from django.conf import settings
import stripe
from django.urls import reverse
from django.contrib import messages
# Create your views here.
stripe.api_key=settings.STRIPE_SECRET_KEY

def home(request):
    return render(request,'home.html')

def contact(request):
    return render(request,'contact.html')

def product(request):
    case=Product.objects.all()
    return render(request,'product.html',{'product':case})

def register_view(request):
    form=CustomUserCreationForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save()    
        return redirect('login')
    return render(request,'register.html',{'form':form})

def login_view(request):
    form=EmailLoginForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.get_user()
        login(request,user)
        return redirect('home')
    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')    

@login_required
def add_cart(request,case_id):
    case=get_object_or_404(Product,id=case_id)
    cart_item,created=Cart.objects.get_or_create(user=request.user,product=case)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('viewcart')


@login_required
def view_cart(request):
    orders = Cart.objects.filter(user=request.user) # Convert to list
    for order in orders:
        order.item_total = order.product.price * order.quantity
    grand_total = sum(order.item_total for order in orders)
    return render(request,'view_cart.html',{'case':orders, 'grand_total': grand_total})


@login_required
def delete_cart(request,case_id):
    item=get_object_or_404(Cart,id=case_id,user=request.user)
    if item.quantity:
        item.delete()
    return redirect('viewcart')
    
@login_required
def purchase_view(request):
    cart_items=Cart.objects.filter(user=request.user)
    total=sum(item.product.price * item.quantity for item in cart_items )

    if request.method == 'POST':
        address=request.POST.get('address')
        phone=request.POST.get('phone','')
        iphone_model=request.POST.get('iphone_model')
        

        if not phone.isdigit() or len(phone) != 10 or phone[0] not in '6789':
            messages.error(request, "Enter a valid 10-digit Indian mobile number")
            return render(request, 'purchase.html', {
                'cart_items': cart_items,
                'total': total
            })

        line_items = []
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            })
        success_url = request.build_absolute_uri(reverse('success'))
        cancel_url = request.build_absolute_uri(reverse('cancel'))

        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        request.session['address'] = address
        request.session['iphone_model'] = iphone_model
        request.session['phone']=phone

        return redirect(session.url)

    return render(request,'purchase.html',{'cart_items':cart_items,'total':total})

def success(request):
    cart_items=Cart.objects.filter(user=request.user)
    
    address = request.session.get('address')
    phone=request.session.get('phone')
    iphone_model = request.session.get('iphone_model')

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            address=address,
            phone=phone,
            iphone_model=iphone_model,
            total_amount=item.product.price * item.quantity,
            payment_method='CARD',
            paid=True
        )
     # Clear cart
    cart_items.delete()

    # Clear session
    # request.session.flush()

    return render(request, 'success.html')


# ✅ Cancel page
def cancel(request):
    return render(request, 'cancel.html')

@login_required
def order_view(request):
    oredered_items=Order.objects.filter(user=request.user)
    for i in oredered_items:
        i.product.price =i.product.price * i.quantity
    return render(request,'oredered.html',{'ordered':oredered_items})

@login_required
def increase_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('viewcart')


@login_required
def decrease_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  

    return redirect('viewcart')






# @login_required
# def buy_now(request, case_id):
    
#     cart_item = get_object_or_404(Cart,id=case_id,user=request.user)

#     product = cart_item.product
#     quantity = cart_item.quantity

#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[
#             {
#                 'price_data': {
#                     'currency': 'inr',
#                     'product_data': {
#                         'name': product.name,
#                     },
#                     'unit_amount': int(product.price * 100),
#                 },
#                 'quantity': quantity,
#             }
#         ],
#         mode='payment',
#         success_url=request.build_absolute_uri(reverse('success')),
#         cancel_url=request.build_absolute_uri(reverse('cancel')),
#     )

#     return redirect(session.url)



# def success(request):
#     return render(request,'success.html')

# def cancel(request):
#     return render(request,'cancel.html')


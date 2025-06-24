from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import  Newsletter
from Products.models import Products
from rest_framework import serializers
from rest_framework import viewsets
from .serializers import UserSerializer, NewsletterSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from Products.serializers import ProductsSerializer
from Carts.serializers import Buy_itemsSerializer, Order_itemsSerializer
from Carts.models import Buy_items, Order_items
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse

# Create your views here.
    
    
# product Api
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    authentication_classes = [JWTAuthentication]
    passion_classes = [permissions.IsAuthenticatedOrReadOnly]

#Newsletter Api
class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
# Buy items Api
class Buy_itemsViewSet(viewsets.ModelViewSet):
    queryset = Buy_items.objects.all()
    serializer_class = Buy_itemsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Order Api
class Order_itemsViewSet(viewsets.ModelViewSet):
    queryset = Order_items.objects.all()
    serializer_class = Order_itemsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@login_required
def api_views(request):
    return redirect('/api/token')


# ---------------------


# Home page
def Home(request):
    context = {
        'products': Products.objects.all()
    }
    return render(request, 'Home/index.html', context)

# Signup page
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Check if the become_seller checkbox was checked
        become_seller = request.POST.get('become_seller', '') == 'on'
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('signup')
            
            elif become_seller:
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name, is_staff=True)
                user.save()
                messages.info(request, 'Seller account created successfully')
                return redirect('login')
            
            else:
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name, is_staff=False)
                user.save()
                messages.info(request, 'User account created successfully')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
        
    return render(request, 'Home/signup.html')



# Login page
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'Home/login.html')

#Newsletter
def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if email already exists in the Newsletter model
        if Newsletter.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists in our newsletter.')
        else:
            # Create a new Newsletter instance and save it
            newsletter = Newsletter(email=email)
            newsletter.save()
            messages.success(request, "You have been added to our newsletter!")
        return redirect('home')
    else:
        return redirect('home')
    
 
 
# make sure to add this in settings.py
# make sure convert price to integer
# make sure requirements.txt is added    
    
#Payment
# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# @login_required
# def initiate_payment(request):
#     if request.method == "POST":

#         cart_items = Buy_items.objects.filter(user=request.user)
        
#         if not cart_items.exists():
#             messages.error(request, "Your cart is empty")
#             return redirect('cart')

#         total_amount = sum(item.product.product_price * item.quantity for item in cart_items)
#         amount_in_paise = int(total_amount * 100)  
#         currency = "INR"
        

#         receipt = f"receipt_{request.user.id}_{int(time.time())}"


#         razorpay_order = client.order.create({
#             "amount": amount_in_paise,
#             "currency": currency,
#             "receipt": receipt,
#             "payment_capture": "1"
#         })


#         request.session['razorpay_order_id'] = razorpay_order['id']
        
#         context = {
#             "razorpay_key_id": settings.RAZORPAY_KEY_ID,
#             "order_id": razorpay_order['id'],
#             "amount": amount_in_paise,
#             "currency": currency,
#             "cart_items": cart_items,
#             "total_amount": total_amount,
#             "callback_url": request.build_absolute_uri(reverse('payment_callback'))
#         }
#         return render(request, "Carts/payment_page.html", context)

#     return redirect('cart')


# @csrf_exempt
# def payment_callback(request):
#     if request.method == "POST":
#         try:

#             payment_id = request.POST.get('razorpay_payment_id', '')
#             order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
            
#             params_dict = {
#                 'razorpay_order_id': order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }


#             client.utility.verify_payment_signature(params_dict)
            

#             stored_order_id = request.session.get('razorpay_order_id')
            
#             if stored_order_id != order_id:
#                 return HttpResponseBadRequest("Order ID mismatch")
            

#             if request.user.is_authenticated:

#                 cart_items = Buy_items.objects.filter(user=request.user)
                

#                 order = Order_items.objects.create(
#                     user=request.user,
#                     payment_id=payment_id,
#                     order_id=order_id,
#                     total_amount=sum(item.product.product_price * item.quantity for item in cart_items),
#                     status="Paid"
#                 )
                

#                 for item in cart_items:
#                     order.products.add(item.product)
#                     order.quantities.append(item.quantity)
#                 order.save()
                

#                 cart_items.delete()
                

#                 if 'razorpay_order_id' in request.session:
#                     del request.session['razorpay_order_id']
                
#                 messages.success(request, "Payment successful! Your order has been placed.")
#                 return redirect('order_success')
            
#             return JsonResponse({"status": "Payment successful!"})
            
#         except razorpay.errors.SignatureVerificationError:
#             return HttpResponseBadRequest("Signature verification failed")
#         except Exception as e:
#             return HttpResponseBadRequest(f"Payment failed: {str(e)}")
            
#     return HttpResponseBadRequest("Invalid request")

# @login_required
# def order_success(request):

#     try:
#         order = Order_items.objects.filter(user=request.user).latest('created_at')
#         context = {
#             'order': order
#         }
#         return render(request, 'Carts/order_success.html', context)
#     except Order_items.DoesNotExist:
#         return redirect('home')
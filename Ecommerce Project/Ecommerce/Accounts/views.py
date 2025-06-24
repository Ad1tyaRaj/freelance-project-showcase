from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Carts.models import Order_items
from decimal import Decimal
# from .forms import AddProductForm

# Create your views here.
# Account page
@login_required
def account_view(request):
    # Get user's order history
    orders = Order_items.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'Accounts/account.html', context)  

# Update profile information
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()     
        messages.success(request, "Profile updated successfully!")
        return redirect('account')
    
    return redirect('account')



# Logout page
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')
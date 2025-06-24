from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Buy_items, Order_items
from decimal import Decimal
from .forms import AddProductForm
from Products.models import Products
from Home.models import Newsletter
# Create your views here.



# Cart related views

def cart_view(request):

    user_items = Buy_items.objects.filter(user=request.user) if request.user.is_authenticated else []
    total_price = sum(item.total_price for item in user_items)
    shipping_cost = Decimal('0.00') if total_price > 50 else Decimal('5.99')
    total_with_shipping = Decimal(total_price) + shipping_cost
    discount_amount = Decimal(request.session.get('discount_amount', '0'))
    active_promo = request.session.get('active_promo', None)
    total_after_discount = total_with_shipping - discount_amount

    context = {
        'products': Products.objects.all(),
        'buy_items': user_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'total_with_shipping': total_with_shipping,
        'discount_amount': discount_amount,
        'total_after_discount': total_after_discount,
        'active_promo': active_promo,
    }
    return render(request, 'Carts/cart.html', context) 

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id) 
    try:

        existing_item = Buy_items.objects.filter(
            user=request.user,
            item_name=product.product_name
        ).first()
        
        if existing_item:

            existing_item.item_quantity += 1
            existing_item.save()
            messages.success(request, f"{product.product_name} quantity updated in your cart!")
        else:


            Buy_items.objects.create(
                user=request.user,
                item_name=product.product_name,
                item_price=product.product_price,
                item_reviews=product.product_reviews,
                item_description=product.product_description,
                item_image=product.product_image,
                item_quantity=1
            )
            messages.success(request, f"{product.product_name} has been added to your cart!")
        
        return redirect('cart')
    
    except Exception as e:
        messages.error(request, f"Error adding product to cart: {str(e)}")
        return redirect('products')

@login_required
def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            quantity = 1
        
        try:
            item = Buy_items.objects.get(id=item_id, user=request.user)
            item.item_quantity = quantity
            item.save()
            messages.success(request, "Cart updated successfully!")
        except Buy_items.DoesNotExist:
            messages.error(request, "Item not found in your cart.")
        except Exception as e:
            messages.error(request, f"Error updating cart: {str(e)}")
            
    return redirect('cart')

@login_required
def remove_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        
        try:
            item = Buy_items.objects.get(id=item_id, user=request.user)
            item.delete()
            messages.success(request, "Item removed from cart!")
        except Buy_items.DoesNotExist:
            messages.error(request, "Item not found in your cart.")
        except Exception as e:
            messages.error(request, f"Error removing item: {str(e)}")
            
    return redirect('cart')

# Buy now page
@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    try:
        
        Buy_items.objects.filter(user=request.user).delete()
        

        buy_item_instance = Buy_items.objects.create(
            user=request.user,
            item_name=product.product_name,
            item_price=product.product_price,
            item_reviews=product.product_reviews,
            item_description=product.product_description,
            item_image=product.product_image,
            item_quantity=1
        )
        
        messages.success(request, f"{product.product_name} has been added to your cart for immediate checkout!")
        return redirect('checkout')
    
    except Exception as e:
        messages.error(request, f"Error with buy now: {str(e)}")
        return redirect('products')

# Promocode
@login_required
def apply_promocode(request):
    if request.method == 'POST':
        promocode = request.POST.get('promo_code')
        

        user_items = Buy_items.objects.filter(user=request.user)
        

        total_price = sum(item.total_price for item in user_items)
        
        if promocode == 'WELCOME10':

            discount_amount = Decimal(total_price) * Decimal('0.1')
            

            request.session['discount_amount'] = str(discount_amount)
            request.session['active_promo'] = {
                'code': 'WELCOME10',
                'description': '10% off your order'
            }
            
            messages.success(request, "Promocode WELCOME10 applied successfully! 10% discount applied.")
        else:
            messages.error(request, "Invalid promocode.")

    return redirect('cart')

# Remove promocode 
@login_required
def remove_promo(request):
     
    if 'discount_amount' in request.session:
        del request.session['discount_amount']
    if 'active_promo' in request.session:
        del request.session['active_promo']
    
    messages.success(request, "Promocode removed successfully!")
    return redirect('cart')


# Checkout page
@login_required
def checkout(request):
    return render(request, 'Carts/account.html')


def become_seller(request):
    return render(request, 'Carts/seller.html') 




def seller_products(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('seller_products')
        else:
            messages.error(request, "Failed to add product. Please try again.")
    else:
        form = AddProductForm()

    context = {
        'form': form,
        'products': Products.objects.all()
    }
    return render(request, 'Carts/seller_product.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('seller_products')
    else:
        form = AddProductForm()
    
    return render(request, 'Carts/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):

    product = get_object_or_404(Products, id=product_id)

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this product.")
        return redirect('seller_products')
    
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('seller_products')
    else:
        form = AddProductForm(instance=product)
    
    return render(request, 'Carts/edit_product.html', {'form': form, 'product': product})





def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('seller_products')

def seller_dashboard(request):
    return render(request, 'Carts/seller_dashboard.html')

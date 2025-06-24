document.addEventListener('DOMContentLoaded', function() {
    // Quantity buttons
    const decreaseButtons = document.querySelectorAll('.quantity-btn.decrease');
    const increaseButtons = document.querySelectorAll('.quantity-btn.increase');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const removeButtons = document.querySelectorAll('.remove-btn');
    
    // Add to cart buttons on recommended products
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    // Decrease quantity
    decreaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-item-id');
            const input = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`);
            let value = parseInt(input.value);
            
            if (value > 1) {
                value--;
                input.value = value;
                updateCartItem(itemId, value);
            }
        });
    });
    
    // Increase quantity
    increaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-item-id');
            const input = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`);
            let value = parseInt(input.value);
            const max = parseInt(input.getAttribute('max'));
            
            if (value < max) {
                value++;
                input.value = value;
                updateCartItem(itemId, value);
            }
        });
    });
    
    // Manual input change
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.getAttribute('data-item-id');
            let value = parseInt(this.value);
            const min = parseInt(this.getAttribute('min'));
            const max = parseInt(this.getAttribute('max'));
            
            if (value < min) {
                value = min;
                this.value = min;
            } else if (value > max) {
                value = max;
                this.value = max;
            }
            
            updateCartItem(itemId, value);
        });
    });
    
    // Remove item
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-item-id');
            removeCartItem(itemId);
        });
    });
    
    // Add to cart from recommended products
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });
    
    // Update cart item quantity
    function updateCartItem(itemId, quantity) {
        fetch('/update-cart-item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                item_id: itemId,
                quantity: quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the cart total and item total
                document.querySelector(`.cart-item[data-item-id="${itemId}"] .cart-total`).textContent = `$${data.item_total}`;
                document.querySelector('.summary-row:first-child span:last-child').textContent = `$${data.cart_total}`;
                document.querySelector('.summary-row.total span:last-child').textContent = `$${data.total_with_shipping}`;
                document.querySelector('.cart-count').textContent = data.cart_items;
                
                // Update shipping if needed
                const shippingElement = document.querySelector('.summary-row:nth-child(2) span:last-child');
                shippingElement.textContent = data.cart_total > 50 ? 'Free' : '$5.99';
            }
        })
        .catch(error => console.error('Error updating cart:', error));
    }
    
    // Remove cart item
    function removeCartItem(itemId) {
        fetch('/remove-cart-item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                item_id: itemId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the item from the DOM
                const cartItem = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
                cartItem.remove();
                
                // Update cart totals
                document.querySelector('.summary-row:first-child span:last-child').textContent = `$${data.cart_total}`;
                document.querySelector('.summary-row.total span:last-child').textContent = `$${data.total_with_shipping}`;
                document.querySelector('.cart-count').textContent = data.cart_items;
                
                // Update shipping if needed
                const shippingElement = document.querySelector('.summary-row:nth-child(2) span:last-child');
                shippingElement.textContent = data.cart_total > 50 ? 'Free' : '$5.99';
                
                // If cart is empty, reload the page to show empty cart message
                if (data.cart_items === 0) {
                    window.location.reload();
                }
            }
        })
        .catch(error => console.error('Error removing item:', error));
    }
    
    // Add to cart
    function addToCart(productId) {
        fetch('/add-to-cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update cart count
                document.querySelector('.cart-count').textContent = data.cart_items;
                
                // Show success message
                showNotification('Product added to cart!', 'success');
                
                // Reload the page if we're on the cart page
                if (window.location.pathname.includes('/cart/')) {
                    window.location.reload();
                }
            } else {
                showNotification(data.message || 'Error adding product to cart', 'error');
            }
        })
        .catch(error => {
            console.error('Error adding to cart:', error);
            showNotification('Error')
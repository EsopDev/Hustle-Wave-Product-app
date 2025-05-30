from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Payment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


# Show available and recently sold products
def product_list(request):
    one_day_ago = timezone.now() - timedelta(days=1)
    products = Product.objects.filter(
        Q(is_sold=False) | Q(is_sold=True, sold_at__gte=one_day_ago)
    ).order_by('-created_at')
    return render(request, 'index.html', {'products': products})


# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sold_message = None
    if product.is_sold:
        sold_message = f"This product was bought by @{product.sold_by.username} on {product.sold_at.strftime('%Y-%m-%d %H:%M:%S')}"
    return render(request, 'detail.html', {
        'product': product,
        'sold_message': sold_message
    })


# Create a new product
@login_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')

        if not all([name, description, price, image, category_id]):
            messages.error(request, "All fields are required.")
            return redirect('create_product')

        category = get_object_or_404(Category, id=category_id)
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            image=image,
            category=category
        )
        messages.success(request, "Product created successfully.")
        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'create.html', {'categories': categories})


# User settings view
@login_required
def settings_view(request):
    return render(request, 'settings.html')


# Delete a product
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('product_list')
    return render(request, 'confirm_delete_product.html', {'product': product})


# Delete user account
@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect('register')
    return render(request, 'confirm_delete_account.html')


# Register view
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if len(password1) < 8 or not any(char.isdigit() for char in password1):
            messages.error(request, "Password must be 8+ chars and include a number.")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('product_list')
        messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


# Add item to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', [])

    if product.is_sold:
        messages.warning(request, "❌ Product already sold.")
        return redirect('product_detail', product_id=product.id)

    if product_id not in cart:
        cart.append(product_id)
        request.session['cart'] = cart
        messages.success(request, f"{product.name} added to cart.")
    return redirect('view_cart')


# View cart
@login_required
def view_cart(request):
    cart_ids = request.session.get('cart', [])
    products_in_cart = Product.objects.filter(id__in=cart_ids)

    total_price = sum(product.price for product in products_in_cart)
    return render(request, 'cart.html', {
        'cart_items': products_in_cart,
        'total_price': total_price
    })


# Remove item from cart
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


# Confirm payment
# Confirm payment and process checkout
@login_required
def confirm_payment(request):
    cart_ids = request.session.get('cart', [])
    cart_items = Product.objects.filter(id__in=cart_ids)

    # Filter out already sold items
    unavailable_items = [item for item in cart_items if item.is_sold]
    cart_items = [item for item in cart_items if not item.is_sold]

    dispatch_fee = 1500
    total_price = sum(item.price for item in cart_items)
    final_total = total_price + dispatch_fee

    if request.method == 'POST':
        location = request.POST.get('location')

        if not location:
            messages.error(request, "Please enter your delivery location.")
            return redirect('confirm_payment')

        for product in cart_items:
            product.is_sold = True
            product.sold_by = request.user
            product.sold_at = timezone.now()
            product.save()

            Payment.objects.create(
                user=request.user,
                product=product,
                amount=product.price,
                location=location,
                dispatch_fee=dispatch_fee,
                status='Confirmed'
            )

        # Clear cart from session
        request.session['cart'] = []

        # Handle removed items warning
        if unavailable_items:
            removed_names = ", ".join([item.name for item in unavailable_items])
            messages.warning(
                request,
                f"{removed_names} were removed from your cart because they're no longer available."
            )

        messages.success(request, f"✅ Payment successful. Total Paid: ₦{final_total}")
        return redirect('product_list')

    # Render checkout page
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'dispatch_fee': dispatch_fee,
        'final_total': final_total,
        'unavailable_items': unavailable_items,
    })

# View payment status
@login_required
def payment_status(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payment_status.html', {'payment': payment})


# User's payment history
@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'payment_history.html', {'payments': payments})


# Admin-only view to check all payments
@staff_member_required
def admin_payments(request):
    payments = Payment.objects.all().order_by('-timestamp')
    return render(request, 'admin_payments.html', {'payments': payments})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



def product_list(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'detail.html', {'product': product})

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')

        category = Category.objects.get(id=category_id)
        product = Product(name=name, description=description, price=price, image=image, category=category)
        product.save()
        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'create.html', {'categories': categories})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create(username=username, email=email)
            user.set_password(password1)
            user.save()
            return redirect('login')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect("login")
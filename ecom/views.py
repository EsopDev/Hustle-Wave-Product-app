from django.shortcuts import render, redirect
from .models import Product, Category


def product_list(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

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
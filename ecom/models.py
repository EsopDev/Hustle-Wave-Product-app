from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields for sold status tracking
    is_sold = models.BooleanField(default=False)  # renamed for clarity
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sold_products')
    sold_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)  # delivery location
    dispatch_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # When payment is completed, mark product as sold
        if self.status == 'Completed' and not self.product.is_sold:
            self.product.is_sold = True
            self.product.sold_by = self.user
            self.product.sold_at = timezone.now()
            self.product.save()
        super().save(*args, **kwargs)

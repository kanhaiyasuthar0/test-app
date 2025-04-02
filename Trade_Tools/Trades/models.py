from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    types = models.CharField(max_length=200 , default="product")
    price = models.CharField(max_length=100 , default="")
    discount_percent = models.CharField(max_length=10 , default="")
    description = models.CharField(max_length=200 , default="")
    image = models.ImageField(upload_to='images/' ,default="")
    image1 = models.ImageField(upload_to='images/' ,default="")
    image2 = models.ImageField(upload_to='images/' ,default="")
    image3 = models.ImageField(upload_to='images/' ,default="")
    image4 = models.ImageField(upload_to='images/' ,default="")
    image5 = models.ImageField(upload_to='images/' ,default="")
    zipfile = models.FileField(upload_to='zipfiles/')

    def __str__(self):
        return self.title

    def actual_price(self):
        try:
            price = float(self.price)
            discount = float(self.discount_percent)
            return int(price - (price * discount / 100))
        except ValueError:
            return "Invalid price or discount"



class Payment(models.Model):
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4().hex)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer_name = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=100, default="")
    customer_email = models.EmailField(default="")
    customer_phone = models.CharField(max_length=15, default="")
    copun_code = models.CharField(max_length=50, default="")
    payment_status = models.CharField(max_length=20, default="Pending")  # 'Pending', 'Success', 'Failed'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        default=1  # Replace `1` with the ID of the default user
    )



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


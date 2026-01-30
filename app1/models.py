from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    cover=models.ImageField(upload_to='covers/',blank=True,null=True)

    def __str__(self):
        return f'{self.name} - {self.model}'


class User(AbstractUser):
    username=models.CharField(max_length=50,blank=True,null=True,unique=False)
    email=models.EmailField(max_length=150,unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return f"{self.email}"
    

    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    cover=models.ImageField(null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.quantity})'
    

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.TextField(default='Not Provided')
    phone=models.CharField(max_length=15)
    iphone_model = models.CharField(max_length=50)
    payment_method=models.CharField(max_length=50,default='CARD')
    total_amount=models.IntegerField(default=0)
    paid=models.BooleanField(default=False)
    ordered_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} ordered {self.product}'


from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('Customer', 'customer'),
        ('Agent', 'agent'),
        
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,default='customer',null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    

    objects = CustomUserManager()



class office(models.Model):
     CATEGORY_CHOICES = [
        ('reception', 'Reception'),
        ('meeting_room', 'Meeting Room'),
        ('pantry', 'Pantry'),
        ('bathroom', 'Bathroom'),
    ]
     Name = models.CharField(max_length=100,unique=True)
     photo = models.URLField(max_length=10000)
     Category = models.CharField(max_length=100,choices=CATEGORY_CHOICES)
     price = models.DecimalField(max_digits=10,decimal_places=2)
     Description = models.TextField()



class Home(models.Model):
     CATEGORY_CHOICES = [
        ('kitchen', 'Kitchen'),
        ('bedroom', 'Bed Room'),
        ('bathroom', 'Bath Room'),
        ('diningroom', 'Dining Room'),
        ('visitingroom', 'Visitingroom'),
        ('kids room', 'Kids Room')
    ]
     Name = models.CharField(max_length=100,unique=True)
     photo = models.URLField(max_length=10000)
     Category = models.CharField(max_length=100,choices=CATEGORY_CHOICES)
     price = models.DecimalField(max_digits=10,decimal_places=2)
     Description = models.TextField()

class Product(models.Model):
     Name = models.CharField(max_length=100)
     photo = models.URLField(max_length=10000)
     description = models.TextField()
     price = models.DecimalField(max_digits=10,decimal_places=2)
     quantity = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(Product, through='CartItem')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def update_total_price(self):
        total_price = sum(item.total_price for item in self.cartitem_set.all())
        self.total_price = total_price
        self.save()


    def clear_cart(self):
        self.cartitem_set.all().delete()

        self.total_price = 0.00
        self.save()




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.Name} in cart for {self.cart.user.username}"

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)
        self.cart.update_total_price()

        
class AgentProduct(models.Model):
    CATEGORY_CHOICES1 = [
        ('home', 'Home'),
        ('office', 'Office'), ]
    CATEGORY_CHOICES2=[
        ('kitchen','Kitchen'),
        ('bathroom','Bathroom'),
        ('bedroom','Bedroom'),
        ('diningroom','Diningroom'),
        ('reception','Reception'),
        ('pantry','Pantry'),
        ('meetingroom','Meetingroom'),

    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'user_type':'Agent'},
    related_name='customer_products' ,null=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to= 'agent_photos',null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    propertytype = models.CharField(max_length=1000,choices=CATEGORY_CHOICES1,null=True)
    catgory = models.CharField(max_length=100,choices=CATEGORY_CHOICES2,null=True)
    
    
    def __str__(self):
        return self.name


class OFFiceBookDesign(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'user_type': 'Customer'},null=True )
    product = models.ForeignKey(office, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.TextField(max_length=10000,null = True)
    contact_no = models.BigIntegerField(null=True)
    address = models.TextField(null=True)

    
class HomeBookDesign(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'user_type': 'Customer'},null=True )
    product = models.ForeignKey(Home, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.TextField(max_length=10000,null = True)
    contact_no = models.BigIntegerField(null=True)
    address = models.TextField(null=True)


class AgentProductBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'user_type': 'Customer'},null=True )
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_created', limit_choices_to={'user_type': 'Agent'}, null=True)
    product = models.ForeignKey(AgentProduct, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.TextField(max_length=10000,null = True)
    contact_no = models.BigIntegerField(null=True)
    address = models.TextField(null=True)







class ContactUS(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'user_type': 'Customer'},null=True )
    name = models.CharField(max_length=200)
    email = models.EmailField()
    contact_no = models.BigIntegerField(null=True)
    description = models.TextField(null=True)


class ListWish(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,limit_choices_to={'user_type': 'Customer'},null=True )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class ProductBuy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Customer'}, null=True)
    name = models.CharField(max_length=200)
    apartment = models.CharField(max_length=200) 
    place = models.CharField(max_length=200)
    pincode = models.IntegerField()
    phone_number = models.BigIntegerField()
    quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)


    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        self.product.quantity -= self.quantity
        self.product.save()
        super(ProductBuy, self).save(*args, **kwargs)









        












class OrderDetail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=255)
    apartment = models.CharField(_('Apartment'), max_length=255)
    pincode = models.CharField(_('Pincode'), max_length=10)
    place = models.CharField(_('Place'), max_length=255)
    phone_no = models.CharField(_('Phone Number'), max_length=15)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Quantity'), default=0)
    total_price = models.DecimalField(_('Total Price'), decimal_places=2, max_digits=10, default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Order Detail')
        verbose_name_plural = _('Order Details')

    def __str__(self):
        return f"{self.quantity} x {self.product.Name} ordered by {self.user.username}"
from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings


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

    def _str_(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.cart.user.username}"

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)
        self.cart.update_total_price()




    







class AgentProduct(models.Model):
    CATEGORY_CHOICES1 = [
        ('home', 'Home'),
        ('shop', 'Shop'),
        ('office', 'Office'),
        
     ]
    CATEGORY_CHOICES2=[
        ('kitchen','Kitchen'),
        ('bathroom','Bathroom'),
        ('bedroom','Bedroom'),
        ('diningroom','Diningroom'),
        ('reception','Reception'),
        ('pantry','Pantry'),
        ('meetingroom','Meetingroom'),
        ('shoproom','Shoproom')
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



class NeededProducts(models.Model):
    CATREGORY_CHOICES= [
        ('bookshelves','Bookshelves'),
        ('centertable','Centertable'),
        ('lcd display unit','LCD Display Unit'),
        ('living-dining-partition','Living-Dining Partition'),
        ('prayer unit','Prayer Unit'),
        ('shoe rack','Shoe Rack'),
        ('sofa and single chairs','Sofa and Single Chairs'),
        ('bed','Bed'),
        ('dressing unit','Dressing Unit'),
        ('wardrobe','Wardrobe'),
        ('bar counter','Bar Counter'),
        ('crockery shelf','Crockery Shelf'),
        ('dining chair','Dining Chair'),
        ('dining table','Dining Table'),
        ('wash','Wash'),
        ('study unit','Study Unit'),
        ('wardrobe cum study table','Wardrobe Cum Study Table'),
    ]
    name = models.CharField(max_length=100)
    photo = models.URLField(max_length=10000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    catgory = models.CharField(max_length=100,choices=CATREGORY_CHOICES,null=True)






class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Customer'},null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)



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




class CartBuy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Customer'}, null=True)
    product = models.ForeignKey(Cart,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    name = models.CharField(max_length=200)
    apartment = models.CharField(max_length=200) 
    place = models.CharField(max_length=200)
    pincode = models.IntegerField()
    phone_number = models.BigIntegerField()


    def save(self, *args, **kwargs):
        cart_instance = self.product
        total_price = cart_instance.total_price
        self.total_price = total_price

        super().save(*args, **kwargs)


class CartBuyItem(models.Model):
    cart_buy = models.ForeignKey(CartBuy, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)



class Order_Items(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)

        


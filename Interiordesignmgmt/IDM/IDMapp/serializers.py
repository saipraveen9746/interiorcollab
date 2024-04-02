from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


from .models import Cart_Buy, office,Home,Product,CartItem,Cart,Order,CustomUser,AgentProduct,OFFiceBookDesign,HomeBookDesign,AgentProductBooking,ListWish,ContactUS,ProductBuy,CartBuy,Order_Items,CartBuyItem
from IDMapp import models

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email' , 'user_type']  
        extra_kwargs = {'password': {'write_only': True}}
    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use.")
        return email

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return password

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type = validated_data['user_type']
        
        )
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = office
        fields = '__all__'


class ProductListserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cart = CartItemSerializer(many=True, read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = models.CartItem
        fields = ['id', 'cart', 'product','quantity']









class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class AgentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProduct
        fields = ['id','name', 'photo', 'price', 'description', 'propertytype', 'catgory',]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    


from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'user']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)
    


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = office
        fields = '__all__'

class OFFiceBookDesignSerializer(serializers.ModelSerializer):
    product = OfficeSerializer(read_only=True)
    class Meta:
        model = OFFiceBookDesign
        fields = ['name', 'email', 'contact_no', 'address','product']

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'

class HomeBookDesignSerializer(serializers.ModelSerializer):
    product = HomeSerializer(read_only=True)
    class Meta:
        model = HomeBookDesign
        fields = ['name', 'email', 'contact_no', 'address','product']

class AgentbookSerializer(serializers.ModelSerializer):
    product = AgentProductSerializer(read_only=True)
    class Meta:
        model = AgentProductBooking
        fields = ['name', 'email', 'contact_no', 'address','product']

class OfficeDetailserializer(serializers.ModelSerializer):
    class Meta:
        model = office
        fields = '__all__'

class HomeDetailserializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'





class AgentUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.user_type.lower() == 'agent':
            return data
        return None 
    
class AgentDetailserializer(serializers.ModelSerializer):
    user = AgentUsernameSerializer(read_only=True)
    class Meta:
        model = AgentProduct
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListWish
        fields = ['user','id','product']
class WishLIstViewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ListWish
        fields ='__all__'




class ContactUSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUS
        fields = ('id', 'name', 'email', 'contact_no', 'description')

    def create(self, validated_data):
        return ContactUS.objects.create(**validated_data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']



class AgentProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProduct
        fields = ['id','user','name','photo','price','description','propertytype','catgory']








# class ProductItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()

#     class Meta:
#         model = ProductItem
#         fields = ['product', 'quantity']

class ProductBuySerializer(serializers.ModelSerializer):
    # items = ProductItemSerializer(many=True)

    class Meta:
        model = ProductBuy
        fields = [ 'name', 'apartment', 'place', 'pincode', 'phone_number','quantity','product']

    def create(self, validated_data):
        # Assuming 'product' is included in the request data
        product = validated_data.pop('product',None)
        quantity = validated_data.pop('quantity',None)

        if product is None:
            raise serializers.ValidationError("Product is required.")
        if quantity is None:
            raise serializers.ValidationError("Quantity is required.")

        # Calculate total price based on the product and quantity
        total_price = product.price * quantity

        # Create the ProductBuy instance
        product_buy = ProductBuy.objects.create(product=product, quantity=quantity, total_price=total_price, **validated_data)
        return product_buy
    

class CartBuyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartBuyItem
        fields = ['product', 'quantity', 'price']
        extra_kwargs = {
            'product': {'required': False}  # Marking product field as not required
        }
        
        

class CartBuySerializer(serializers.ModelSerializer):
    items = CartBuyItemSerializer(many=True, read_only=True)
    class Meta:
        model = CartBuy
        fields = '__all__'



class Cart_BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Buy
        fields = '__all__'


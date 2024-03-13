from rest_framework import serializers
from django.contrib.auth.models import User


from .models import office,Home,Product,CartItem,Cart,Order,CustomUser,AgentProduct,OfficeBookDesign
from IDMapp import models


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'user_type']  
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']


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
    productname = serializers.CharField(source='product.Name', read_only=True)
    class Meta:
        model = models.CartItem
        fields = [ 'cart', 'productname', 'quantity']









class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class AgentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProduct
        fields = ['name', 'photo', 'price', 'description', 'propertytype', 'catgory',]

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



class OfficeBookDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeBookDesign
        fields = ['name', 'email', 'contact_no', 'address']



import time
from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import  UserRegistrationSerializer,OfficeSerializer
from .models import Order, office,Home,Product,Cart,CartItem,AgentProduct,CustomUser
from .serializers import ProductListserializer,ProductDetailserializer,CartSerializer,CompanyNameSerializer,AgentProductSerializer,HomeSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .main import RazorpayClient
from rest_framework import viewsets
from .permissions import AgentPermissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt .tokens import RefreshToken


from IDMapp import models

from IDMapp import serializers

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class OfficeListView(generics.ListAPIView):
    queryset = office.objects.all()
    serializer_class = OfficeSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListserializer
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailserializer
    lookup_field = 'id'




#     def post(self, request, product_id):
#         cart, created = Cart.objects.get_or_create(user=request.user)

#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#         quantity = request.data.get('quantity', 1)

#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         cart_item.quantity += quantity
#         cart_item.save()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
    

class AddToCart(generics.CreateAPIView):
    serializer_class = serializers.CartItemSerializer

    def post(self, request, *args, **kwargs):     
        user = request.user
        product_id = self.kwargs.get('product_id')
        products = get_object_or_404(models.Product, pk=product_id)
        quantity = self.kwargs.get('quantity')
        # print('------------------------------------')
        # print(products)
        if quantity <= products.quantity:
            if not product_id:
                return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                cart = models.Cart.objects.get(user=user)
            except models.Cart.DoesNotExist:
                cart = models.Cart.objects.create(user=user)
            product = models.Product.objects.get(pk=product_id)  
            try:
                cart_item = models.CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
                cart_item.save()
            except models.CartItem.DoesNotExist:
                cart_item = models.CartItem.objects.create(cart=cart, product=product, quantity=quantity)

            serializer = self.get_serializer(cart_item)
        else:
            return Response({'error':'That much product not available'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CartItemsListview(generics.ListAPIView):
    serializer_class=serializers.CartItemSerializer
    queryset=models.CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        query=models.CartItem.objects.filter(cart__user=user)
        return query




class CompanyList(generics.ListAPIView):
    serializer_class=serializers.CompanyNameSerializer
    queryset=models.CustomUser.objects.filter(user_type='agent')
    permission_classes = [IsAuthenticated]



class CompanyProductListView(generics.ListAPIView):
    serializer_class = AgentProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return AgentProduct.objects.filter(user_id=user_id)
    

class AgentProductCreateView(generics.CreateAPIView):
    queryset = AgentProduct.objects.all()




    
    serializer_class = AgentProductSerializer
    permission_classes = [AgentPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 




from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product is not None:
            product.quantity -= instance.quantity
            product.save()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Product
from .serializers import OrderSerializer

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        product_id = kwargs.get('product_id')  # Use kwargs, not request.kwargs
        quantity = kwargs.get('quantity')

        # Get the Product object using get_object_or_404
        product = get_object_or_404(Product, pk=product_id)

        if quantity > product.quantity:
            return Response({'error': 'Not enough quantity available'}, status=status.HTTP_400_BAD_REQUEST)

        order_data = {
            'product': product_id,
            'quantity': quantity,
        }

        serializer = OrderSerializer(data=order_data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            product.quantity -= quantity
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import BookDesign, AgentProduct
from .serializers import BookdesignSerializer

class Bookdesign(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        product_id = kwargs.get('product_id')

        try:
            # Query the AgentProduct based on the provided product_id
            agent_product = AgentProduct.objects.get(id=product_id)
        except AgentProduct.DoesNotExist:
            return Response({'error': 'AgentProduct not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create the BookDesign instance
        book_data = {'agentproduct': agent_product.id}
        serializer = BookdesignSerializer(data=book_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryHomesAPIView(generics.ListAPIView):
    serializer_class = HomeSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Home.objects.filter(Category=category)
    

class CategoryOfficeApiView(generics.ListAPIView):
    serializer_class = OfficeSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return office.objects.filter(Category=category)
    

class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'user_type' : user.user_type
                


    
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
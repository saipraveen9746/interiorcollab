import time
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from .serializers import   OrderDetailSerializer, UserRegistrationSerializer,OfficeSerializer
from .models import ContactUS,office,Home,Product,Cart,CartItem,AgentProduct,CustomUser,HomeBookDesign,AgentProductBooking,ListWish
from .serializers import ProductListserializer,ProductDetailserializer,CartSerializer,CompanyNameSerializer,AgentProductSerializer,HomeSerializer,AgentbookSerializer,OfficeDetailserializer,HomeDetailserializer,AgentDetailserializer,CartItemSerializer,WishListSerializer,OFFiceBookDesign,ContactUSSerializer,CustomUserSerializer,AgentProductDetailsSerializer,ProductBuySerializer
from .serializers import OFFiceBookDesignSerializer,HomeBookDesignSerializer,WishLIstViewSerializer,CartIItemSerializer
from rest_framework.views import APIView
from .models import ProductBuy
from rest_framework.permissions import IsAuthenticated
from .main import RazorpayClient
from rest_framework import viewsets
from .permissions import AgentPermissions,IsCustomer
from django.contrib.auth import authenticate
from rest_framework_simplejwt .tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from IDMapp import models
from IDMapp import serializers
from rest_framework.viewsets import ModelViewSet,ViewSet
from django.db.models.signals import post_save
from django.dispatch import receiver




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
    

class AddToCart(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartItemSerializer

    def post(self, request, *args, **kwargs):     
        user = request.user
        product_id = self.kwargs.get('product_id')
        products = get_object_or_404(models.Product, pk=product_id)
        quantity = self.kwargs.get('quantity')
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
            return Response([serializer.data],status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'That much product not available'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class RemoveFromCart(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

 
        cart_item = CartItem.objects.filter(cart__user=user, product_id=product_id).first()
        if not cart_item:
            return Response({"error": "Product is not in the cart"}, status=status.HTTP_400_BAD_REQUEST)


        cart_item.delete()


        cart_item.cart.update_total_price()

        return Response({"success": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT)

    

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
    queryset=models.CustomUser.objects.filter(user_type='Agent')
    permission_classes = [IsAuthenticated]



class CompanyProductListView(generics.ListAPIView):
    serializer_class = AgentProductDetailsSerializer
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



class DeleteAgentProduct(generics.DestroyAPIView):
    queryset = AgentProduct.objects.all()
    serializer_class = AgentProductSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": "Agent product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




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
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type' : user.user_type,
               
                


    
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_office(request, office_id):
    Office = get_object_or_404(office, pk=office_id)

    if request.user.user_type != 'Customer':
        return Response({'error': 'Only customers can book office products.'}, status=status.HTTP_403_FORBIDDEN)


    if OFFiceBookDesign.objects.filter(user=request.user, product=Office).exists():
        return Response({'error': 'You have already booked this office product.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = OFFiceBookDesignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=Office)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_home(request, home_id):

    home = get_object_or_404(Home, pk=home_id)


    if request.user.user_type != 'Customer':
        return Response({'error': 'Only customers can book home products.'}, status=status.HTTP_403_FORBIDDEN)


    if HomeBookDesign.objects.filter(user=request.user, product=home).exists():
        return Response({'error': 'You have already booked this office product.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = HomeBookDesignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=home)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





class BookedHomeDetails(generics.ListAPIView):
    serializer_class = serializers.HomeBookDesignSerializer
    queryset = models.HomeBookDesign.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        query = models.HomeBookDesign.objects.filter(user_id=user)
        return query
    


class BookedOfficeDetails(generics.ListAPIView):
    serializer_class = serializers.AgentbookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        queryset = models.AgentProductBooking.objects.filter(product__user_id=self.request.user.id, product__company_id=company_id)
        return queryset
    




    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_agent_product(request, product_id):
    agent_product = get_object_or_404(AgentProduct, pk=product_id)

    if request.user.user_type != 'Customer':
        return Response({'error': 'Only customers can book agent products.'}, status=status.HTTP_403_FORBIDDEN)

    if AgentProductBooking.objects.filter(user=request.user, product=agent_product).exists():
        return Response({'error': 'You have already booked this agent product.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = AgentbookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, agent=agent_product.user, product=agent_product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookedAgentProductDetails(generics.ListAPIView):
    serializer_class = serializers.AgentbookSerializer
    queryset = models.AgentProductBooking.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        query = models.AgentProductBooking.objects.filter(agent_id=user)
        return query



class OfficeDetailView(generics.RetrieveAPIView):
    queryset = office.objects.all()
    serializer_class = OfficeDetailserializer
    lookup_field = 'id'
    
class HomeDetailView(generics.RetrieveAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeDetailserializer
    lookup_field = 'id'


class AgentProductDetailView(generics.RetrieveAPIView):
    queryset = AgentProduct.objects.all()
    serializer_class = AgentDetailserializer
    lookup_field = 'id'






class AddToWishListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, *args, **kwargs):
        user = request.user
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if ListWish.objects.filter(user=user, product=product).exists():
            return Response({"error": "Product is already in the wishlist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Pass partial=True to allow partial updates
        serializer = WishListSerializer(data={'user': user.id, 'product': product_id}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response([serializer.data], status=status.HTTP_201_CREATED)
        else:
            return Response([serializer.errors], status=status.HTTP_400_BAD_REQUEST)
    

    

class WishListView(generics.ListAPIView):
    serializer_class=serializers.WishListSerializer
    queryset=models.ListWish.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        query=models.WishList.objects.filter( user=user)
        return query
    


class WishListView(generics.ListAPIView):
    queryset = ListWish.objects.all()
    serializer_class = WishLIstViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class RemoveFromWishListView(generics.DestroyAPIView):
    queryset = ListWish.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

  
        wish_list_item = ListWish.objects.filter(user=user, product_id=product_id).first()
        if not wish_list_item:
            return Response({"error": "Product is not in the wishlist"}, status=status.HTTP_400_BAD_REQUEST)

     
        wish_list_item.delete()
        return Response({"success": "Product removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contact_us(request):
    if request.method == 'POST':
        # Create a mutable copy of request.data
        mutable_data = request.data.copy()
        # Add user information to mutable_data
        mutable_data['user'] = request.user.id
        serializer = ContactUSSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_type='Agent')
    serializer_class = CustomUserSerializer





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_product(request, product_id):

    customer = get_object_or_404(Product, pk=product_id)

    if request.user.user_type != 'Customer':
        return Response({'error': 'Only customers can buy products.'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
        quantity = int(request.data.get('quantity', 1))
        if customer.quantity < quantity:
            return Response({'error': 'No quantity available.'}, status=status.HTTP_400_BAD_REQUEST)



    if request.method == 'POST':
        serializer = ProductBuySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        order_details = []
        for cart_item in cart_items:
            order_details.append({

                
                'user': user.pk,
                'name': request.data.get('name'),
                'apartment': request.data.get('apartment'),
                'pincode': request.data.get('pincode'),
                'place': request.data.get('place'),
                'phone_no': request.data.get('phone_no'),
                'product': cart_item.product.pk,
                'quantity': cart_item.quantity,
                'total_price': cart_item.total_price
            })

        serializer = OrderDetailSerializer(data=order_details, many=True)
        if serializer.is_valid():
            serializer.save()

            
            for order_detail in serializer.validated_data:
                product_id = order_detail['product'].id
                ordered_quantity = order_detail['quantity']
                product = Product.objects.get(pk=product_id)
                product.quantity -= ordered_quantity
                product.save()
            

            user.cart.all().delete()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class UpdateCartItem(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartIItemSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        product_id = self.kwargs.get('product_id')
        new_quantity = request.data.get('quantity')

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if new_quantity is None:
            return Response({'error': 'New quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = models.Cart.objects.get(user=user)
        except models.Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        product = get_object_or_404(models.Product, pk=product_id)
        
        try:
            cart_item = models.CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += int(new_quantity)  # Add the new quantity to the existing quantity
            cart_item.save()
            cart.update_total_price()  # Update total price after updating cart item
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

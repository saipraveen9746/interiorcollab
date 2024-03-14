from django import views
from django.urls import path
from .views import  UserRegistrationView,OfficeListView
from .views import ProductListView,ProductDetailView,AddToCart,CartItemsListview,CompanyList,CompanyProductListView,CategoryHomesAPIView,CategoryOfficeApiView
from .views import AgentProductCreateView,PlaceOrderView,Bookdesign,LoginView


urlpatterns = [
    
    
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('office-list/',OfficeListView.as_view(),name='office_list'),
    path('productlist/',ProductListView.as_view(),name='product_list'),
    path('products/<int:id>/',ProductDetailView.as_view(),name='products'),
    path('cartlist/', CartItemsListview.as_view(), name='cart'),
    # path('cart/<int:product_id>/', CartView.as_view(), name='add-to-cart')
    path('AddToCart/<int:product_id>/<int:quantity>/',AddToCart.as_view(),name='AddToCart'),
    path('company-list/', CompanyList.as_view(), name='agent-product-list-create'),
    path('company-products/<int:user_id>/', CompanyProductListView.as_view(), name='company-product-list'),
    path('agent-product/',AgentProductCreateView.as_view(),name='agent-product'),
    path('place_order/<int:product_id>/<int:quantity>/', PlaceOrderView.as_view(), name='place-order'),
    path('book_design/<int:product_id>/',Bookdesign.as_view(), name='book_design'),
    path('homecategory/<str:category>/', CategoryHomesAPIView.as_view(), name='category-homes'),
    path('officecategory/<str:category>/',CategoryOfficeApiView.as_view(),name='category-office'),
    path('login/',LoginView.as_view(),name='login')
    
  


]

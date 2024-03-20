from django import views
from django.urls import path
from .views import  UserRegistrationView,OfficeListView
from .views import ProductListView,ProductDetailView,AddToCart,CartItemsListview,CompanyList,CompanyProductListView,CategoryHomesAPIView,CategoryOfficeApiView
from .views import AgentProductCreateView,PlaceOrderView,LoginView,book_office,book_home,BookedHomeDetails,BookedOfficeDetails,book_agent_product,OfficeDetailView,HomeDetailView,AgentProductDetailView,BookedAgentProductDetails,RemoveFromWishListView
from .views import  AddToWishListView,WishListView,RemoveFromCart,DeleteAgentProduct,contact_us,AgentListView

urlpatterns = [
    
    
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('office-list/',OfficeListView.as_view(),name='office_list'),
    path('productlist/',ProductListView.as_view(),name='product_list'),
    path('products/<int:id>/',ProductDetailView.as_view(),name='products'),
    path('cartlist/', CartItemsListview.as_view(), name='cart'),
    # path('cart/<int:product_id>/', CartView.as_view(), name='add-to-cart')
    path('AddToCart/<int:product_id>/<int:quantity>/',AddToCart.as_view(),name='AddToCart'),
    path('cart/remove/<int:pk>/',RemoveFromCart.as_view(),name='remove-from-cart'),
    path('company-list/', CompanyList.as_view(), name='agent-product-list-create'),
    path('agent-products/<int:user_id>/', CompanyProductListView.as_view(), name='company-product-list'),
    path('agent-product-create/',AgentProductCreateView.as_view(),name='agent-product'),
    path('delete-agent-product/<int:pk>/', DeleteAgentProduct.as_view(), name='delete-agent-product'),
    path('place_order/<int:product_id>/<int:quantity>/', PlaceOrderView.as_view(), name='place-order'),
    path('homecategory/<str:category>/', CategoryHomesAPIView.as_view(), name='category-homes'),
    path('officecategory/<str:category>/',CategoryOfficeApiView.as_view(),name='category-office'),
    path('login/',LoginView.as_view(),name='login'),
    path('officebook/<int:office_id>/book/', book_office, name='book_office_api'),
    path('homebook/<int:home_id>/book/', book_home, name='book_office_api'),
    path('booked_homes/', BookedHomeDetails.as_view(), name='booked_home_details'),
    path('booked_offices/', BookedOfficeDetails.as_view(), name='booked_office_details'),
    path('booked_agent_product/',BookedAgentProductDetails.as_view(), name='booked_agentproduct_details'),
    path('agentproductbooking/<int:product_id>/book/',book_agent_product,name='agentproductbook'),
    path('officedetails/<int:id>/',OfficeDetailView.as_view(),name='officedetails'),
    path('homedetails/<int:id>/',HomeDetailView.as_view(),name='homedetails'),
    path('agentproductdetails/<int:id>/',AgentProductDetailView.as_view(),name='agentproductdetails'),
    path('wishlist/add/<int:product_id>/', AddToWishListView.as_view(), name='add-to-wishlist'),
    path('wishlistview/',WishListView.as_view(),name='wishlistview'),
    path('wishlist/remove/<int:pk>/', RemoveFromWishListView.as_view(), name='remove-from-wishlist'),
    path('contact-us/', contact_us, name='contact_us'),
    path('agent-list-view/',AgentListView.as_view(),name='agent-list-view')
    
    
    


    




]


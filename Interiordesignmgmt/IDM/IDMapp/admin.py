from django.contrib import admin
from .models import office,Home,Product,AgentProduct,CustomUser,ContactUS,OrderDetail

# Register your models here.

admin.site.register(Home)
admin.site.register(CustomUser)
admin.site.register(office)
admin.site.register(Product)
admin.site.register(AgentProduct)

admin.site.register(ContactUS)
admin.site.register(OrderDetail)



from django.urls import path, include
from django import views
from .views import MessageListCreateAPIView,MessageListAPIView





urlpatterns = [
    path('messages/<int:receiver>/',MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('listmessages/<int:receiver_id>/',MessageListAPIView.as_view(), name='message-list-create'),


]

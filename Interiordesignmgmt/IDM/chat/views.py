from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .serializers import MessageSerializer,MessageListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from IDMapp.models import CustomUser
from rest_framework import generics,serializers,permissions
from chat import models
from chat.models import Message



class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        receiver_id = self.kwargs['receiver']
        # Mark messages as read
        messages = models.Message.objects.filter(receiver_id=receiver_id)
        for message in messages:
            message.is_read = True
            message.save()
        return messages
    
    def perform_create(self, serializer):
        receiver_id = self.kwargs.get('receiver')
        receiver = get_object_or_404(models.CustomUser, id=receiver_id)
        serializer.save(sender=self.request.user, receiver=receiver)


class MessageListAPIView(generics.ListCreateAPIView):
    serializer_class =MessageListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')
        return models.Message.objects.filter(sender=user, receiver_id=receiver_id) | \
               models.Message.objects.filter(sender_id=receiver_id, receiver=user)
from rest_framework import serializers
from .models import Message
from IDMapp.models import CustomUser






class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message']

class MessageListSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    class Meta:
        model = Message
        fields = ['sender_username','receiver_username','timestamp','message']  

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']



from rest_framework import serializers
from .models import Message






class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message']

class MessageListSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    class Meta:
        model = Message
        fields = ['sender_username','receiver_username','is_read','timestamp','message']


        

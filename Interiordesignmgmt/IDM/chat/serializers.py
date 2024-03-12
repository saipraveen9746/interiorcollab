from rest_framework import serializers
from .models import Message,ChatRoom

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender', 'sender_name', 'chat_room']

    def get_sender_name(self, obj):
        return obj.sender.username

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'description', 'participants', 'messages']
        depth = 1
        



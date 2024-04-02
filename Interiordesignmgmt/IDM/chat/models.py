

    

from django.db import models
from django.contrib.auth import get_user_model
from IDMapp.models import CustomUser



class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages',null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages',default = 1)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"From: {self.sender} - To: {self.receiver}"
    

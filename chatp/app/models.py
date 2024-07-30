from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    date = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    has_been_seen = models.BooleanField(default=False)
    
    messages = models.TextField()
    
    def __str__(self):
        return self.messages
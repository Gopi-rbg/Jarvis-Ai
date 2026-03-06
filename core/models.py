from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Conversation(models.Model):
    """Model to store conversation history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jarvis_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Conversation - {self.user.username} - {self.created_at}"


class Message(models.Model):
    """Model to store individual messages in a conversation"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('jarvis', 'Jarvis'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    command_detected = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


class JarvisCommand(models.Model):
    """Model to store recognized commands"""
    COMMAND_TYPE_CHOICES = [
        ('website', 'Open Website'),
        ('question', 'Answer Question'),
        ('joke', 'Tell Joke'),
        ('time', 'Get Time'),
        ('search', 'Web Search'),
        ('music', 'Play Music'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jarvis_commands')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    command_text = models.TextField()
    command_type = models.CharField(max_length=20, choices=COMMAND_TYPE_CHOICES)
    response = models.TextField()
    executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.command_type}: {self.command_text[:50]}"

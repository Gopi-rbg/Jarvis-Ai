from rest_framework import serializers
from .models import Conversation, Message, JarvisCommand


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'command_detected', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'created_at', 'updated_at', 'messages']


class JarvisCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = JarvisCommand
        fields = ['id', 'command_text', 'command_type', 'response', 'executed', 'created_at']

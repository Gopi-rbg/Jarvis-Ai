from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import json
import json
from datetime import datetime
import re

from .models import Conversation, Message, JarvisCommand
from .serializers import ConversationSerializer, MessageSerializer, JarvisCommandSerializer

# Create your views here.

def index(request):
    """Main Jarvis dashboard page"""
    return render(request, 'core/index.html')


def dashboard(request):
    """Dashboard page (requires login)"""
    if not request.user.is_authenticated:
        return render(request, 'core/login.html')
    return render(request, 'core/dashboard.html')


@login_required
def get_conversation_history(request):
    """Get conversation history for the current user"""
    conversations = Conversation.objects.filter(user=request.user)
    serializer = ConversationSerializer(conversations, many=True)
    return JsonResponse({'conversations': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_command(request):
    """Process voice command and return response from Jarvis"""
    try:
        data = json.loads(request.body)
        user_text = data.get('text', '').strip()
        
        if not user_text:
            return Response({'error': 'No text provided'}, status=400)
        
        # Get or create conversation
        conversation = Conversation.objects.create(user=request.user)
        
        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_text
        )
        
        # Parse and execute command
        command_type, response, command_text = parse_and_execute_command(user_text, request.user)
        
        # Save Jarvis response
        jarvis_message = Message.objects.create(
            conversation=conversation,
            role='jarvis',
            content=response,
            command_detected=command_text
        )
        
        # Log the command
        JarvisCommand.objects.create(
            user=request.user,
            message=user_message,
            command_text=command_text or user_text,
            command_type=command_type,
            response=response,
            executed=True
        )
        
        return Response({
            'response': response,
            'command_type': command_type,
            'command_text': command_text,
            'conversation_id': conversation.id,
            'timestamp': timezone.now().isoformat()
        })
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)


def parse_and_execute_command(text, user):
    """Parse user command and generate appropriate response"""
    text_lower = text.lower()
    
    # Remove wake word if present
    if text_lower.startswith('jarvis'):
        text_lower = text_lower[6:].strip()
    
    command_type = 'other'
    command_text = text_lower
    
    # Website opening commands
    website_commands = {
        'youtube': ('https://www.youtube.com', 'Opening YouTube'),
        'google': ('https://www.google.com', 'Opening Google'),
        'github': ('https://www.github.com', 'Opening GitHub'),
        'linkedin': ('https://www.linkedin.com', 'Opening LinkedIn'),
        'twitter': ('https://www.twitter.com', 'Opening Twitter'),
        'facebook': ('https://www.facebook.com', 'Opening Facebook'),
    }
    
    for site, (url, response_msg) in website_commands.items():
        if site in text_lower:
            command_type = 'website'
            return command_type, f"{response_msg} for you. Opening in a new tab.", f"open {site}"
    
    # Time commands
    if any(word in text_lower for word in ['time', 'what time', 'tell me the time']):
        current_time = datetime.now().strftime("%I:%M %p")
        command_type = 'time'
        return command_type, f"The current time is {current_time}.", "get time"
    
    # Joke commands
    if any(word in text_lower for word in ['joke', 'tell me a joke', 'make me laugh']):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "Why do Java developers wear glasses? Because they don't C#!",
            "How many MySQL developers does it take to change a light bulb? None, that's not their function.",
            "Why did the developer go broke? Because he used up all his cache!",
        ]
        import random
        joke = random.choice(jokes)
        command_type = 'joke'
        return command_type, joke, "tell joke"
    
    # Search commands
    if any(word in text_lower for word in ['search', 'find', 'look up']):
        match = re.search(r'(?:search|find|look up)\s+(?:for\s+)?(.+)', text_lower)
        if match:
            query = match.group(1).strip()
            command_type = 'search'
            return command_type, f"Searching for {query} on Google. Opening search results.", f"search {query}"
    
    # Music commands  
    if any(word in text_lower for word in ['play music', 'play a song', 'music']):
        command_type = 'music'
        return command_type, "Starting music playback. Opening your music player.", "play music"
    
    # Default Q&A response
    command_type = 'question'
    response = generate_ai_response(text_lower, user)
    return command_type, response, text_lower


def generate_ai_response(question, user):
    """Generate AI response using OpenAI API or fallback responses"""
    # Fallback responses for common questions
    fallback_responses = {
        'hello': "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
        'hi': "Hi there! Ready to assist you. What can I do for you?",
        'what is python': "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation.",
        'what is django': "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It's perfect for building scalable web applications.",
        'who are you': "I'm Jarvis, your personal AI assistant. I can help you open websites, answer questions, tell jokes, and much more!",
        'what can you do': "I can help you open websites like YouTube and Google, answer questions, tell jokes, show you the time, search the web, and play music!",
    }
    
    # Check for exact or partial matches in fallback responses
    question_lower = question.lower()
    for key, response in fallback_responses.items():
        if key in question_lower:
            return response
    
    # Try to use OpenAI API if configured
    api_key = settings.JARVIS_CONFIG.get('OPENAI_API_KEY')
    if api_key and api_key != 'your-openai-api-key':
        try:
            import openai
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Keep responses concise and friendly."},
                    {"role": "user", "content": question}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
    
    # Fallback generic response
    return f"That's an interesting question about '{question}'. I'm still learning, but I'd be happy to help you search for more information about this topic!"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation(request, conversation_id):
    """Get details of a specific conversation"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        conversation.delete()
        return Response({'success': 'Conversation deleted'})
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_commands(request):
    """Get user's command history"""
    commands = JarvisCommand.objects.filter(user=request.user).order_by('-created_at')[:50]
    serializer = JarvisCommandSerializer(commands, many=True)
    return Response({'commands': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_history(request):
    """Clear user's conversation history"""
    try:
        Conversation.objects.filter(user=request.user).delete()
        JarvisCommand.objects.filter(user=request.user).delete()
        return Response({'success': 'History cleared'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

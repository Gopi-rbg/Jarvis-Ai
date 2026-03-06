from django.contrib import admin
from .models import Conversation, Message, JarvisCommand

# Register your models here.

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'message_count')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'content_preview', 'timestamp')
    list_filter = ('role', 'timestamp', 'conversation__user')
    search_fields = ('content', 'conversation__user__username')
    readonly_fields = ('timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(JarvisCommand)
class JarvisCommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'command_type', 'command_preview', 'executed', 'created_at')
    list_filter = ('command_type', 'executed', 'created_at', 'user')
    search_fields = ('command_text', 'user__username')
    readonly_fields = ('created_at',)

    def command_preview(self, obj):
        return obj.command_text[:50] + '...' if len(obj.command_text) > 50 else obj.command_text
    command_preview.short_description = 'Command'

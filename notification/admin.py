from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'email_sent', 'read', 'created_at')
    list_filter = ('notification_type', 'email_sent', 'read', 'created_at')
    search_fields = ('user__email', 'user__username', 'title', 'message')
    readonly_fields = ('created_at', 'updated_at', 'email_sent_at', 'read_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Notification Details', {
            'fields': ('notification_type', 'title', 'message')
        }),
        ('Email Status', {
            'fields': ('email_sent', 'email_sent_at')
        }),
        ('Read Status', {
            'fields': ('read', 'read_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

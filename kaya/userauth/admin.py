from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserDevice


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'phone', 'roles', 'is_active', 
        'is_blocked', 'is_archived', 'date_joined'
    ]
    list_filter = [
        'roles', 'is_active', 'is_blocked', 'is_archived', 
        'is_staff', 'date_joined', 'provider'
    ]
    search_fields = ['phone']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']

    fieldsets = (
        (None, {
            'fields': ('phone',)
        }),
        ('Personal Info', {
            'fields': ('provider',)
        }),
        ('Permissions', {
            'fields': ('roles', 'is_active', 'is_staff', 'is_superuser', 
                       'is_blocked', 'is_archived', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'roles'),
        }),
    )
    
    actions = ['make_active', 'make_inactive', 'block_users', 'unblock_users', 'archive_users', 'unarchive_users']

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} users marked as active.")
    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} users marked as inactive.")
    make_inactive.short_description = "Mark selected users as inactive"

    def block_users(self, request, queryset):
        updated = queryset.update(is_blocked=True)
        self.message_user(request, f"{updated} users blocked.")
    block_users.short_description = "Block selected users"

    def unblock_users(self, request, queryset):
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f"{updated} users unblocked.")
    unblock_users.short_description = "Unblock selected users"

    def archive_users(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, f"{updated} users archived.")
    archive_users.short_description = "Archive selected users"

    def unarchive_users(self, request, queryset):
        updated = queryset.update(is_archived=False)
        self.message_user(request, f"{updated} users unarchived.")
    unarchive_users.short_description = "Unarchive selected users"


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'last_updated', 'get_user_status']
    list_filter = ['device_type', 'last_updated']
    search_fields = ['user__phone', 'fcm_token']
    readonly_fields = ['last_updated']
    raw_id_fields = ['user']

    def get_user_status(self, obj):
        color = '#28a745' if obj.user.is_active else '#dc3545'
        status = 'Active' if obj.user.is_active else 'Inactive'
        return format_html(
            '<span style="color: {};">{}</span>',
            color, status
        )
    get_user_status.short_description = 'User Status'

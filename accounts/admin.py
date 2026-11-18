from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('user_id', 'email', 'username', 'full_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'full_name')
    ordering = ('-created_at',)
    fieldsets = UserAdmin.fieldsets + (
        ('ClaimKeep Profile & Role', {
            'fields': ('full_name', 'role', 'contact_number', 'profile_photo')
        }),
    )
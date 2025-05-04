from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_superuser', 'avatar_preview']
    list_filter = ['role', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name']
    readonly_fields = ['avatar_preview']

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Thông tin thêm", {
            'fields': ('role', 'avatar', 'avatar_preview')
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.avatar.url)
        return "(Không có)"
    avatar_preview.short_description = 'Avatar'

admin.site.register(User, UserAdmin)


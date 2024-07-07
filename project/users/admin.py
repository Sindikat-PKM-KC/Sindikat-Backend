from django.contrib import admin
from .models import User, EmergencyContact
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    list_display = ("email", "name", "is_staff")
    search_fields = ("email", "name", )
    ordering = ("email",)


class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "user")


admin.site.register(User, CustomUserAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)

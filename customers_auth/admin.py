from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from customers_auth.models import Customer
from django.utils.translation import gettext_lazy as _

# Register your models here.
class CustomerUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username","email", "password")}),
        (_("Personal info"), {"fields": ("phone", "address1","address2")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email","username","is_staff")
    search_fields = ("email","username")
    ordering = ("username","email",)
   
# Register Custom User model with Custom User manager Class.

admin.site.register(Customer, CustomerUserAdmin)
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.apps import apps as django_apps

from collection_service.users.forms import UserAdminChangeForm, UserAdminCreationForm
from collection_service.users.models import Service

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
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
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


class ServiceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ["origin"]}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "user_permissions"
                ),
            },
        )
    )
    list_display = ["origin"]
    filter_horizontal = (
        "user_permissions",
    )

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.username = obj.origin
        super().save_model(request, obj, form, change)

svc = django_apps.get_model("users.Service", require_ready=False)
admin.site.register(Service, ServiceAdmin)

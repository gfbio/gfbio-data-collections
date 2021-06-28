from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "nfdi_collection.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import nfdi_collection.users.signals  # noqa F401
        except ImportError:
            pass

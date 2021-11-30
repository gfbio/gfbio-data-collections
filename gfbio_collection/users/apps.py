from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "gfbio_collection.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import gfbio_collection.users.signals  # noqa F401
        except ImportError:
            pass

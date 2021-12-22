from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "gfbio_collections.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import gfbio_collections.users.signals  # noqa F401
        except ImportError:
            pass

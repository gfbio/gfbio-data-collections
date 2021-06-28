from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DataIdConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = "nfdi_collection.dataid"
    verbose_name = _("DataID")

    def ready(self):
        try:
            import nfdi_collection.dataid.signals  # noqa F401
        except ImportError:
            pass

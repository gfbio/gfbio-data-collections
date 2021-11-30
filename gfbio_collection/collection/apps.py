from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CollectionConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = "gfbio_collection.collection"
    verbose_name = _("Collection")

    def ready(self):
        try:
            import gfbio_collection.collection.signals  # noqa F401
        except ImportError:
            pass

from django.contrib import admin
from collection_service.collection import models


class CollectionAdmin(admin.ModelAdmin):
    list_filter = ('service',)
    search_fields = ['id', 'external_user_id']
    date_hierarchy = 'created'

    list_display = ('id', 'external_user_id', 'service', 'created', 'modified')

admin.site.register(models.Collection, CollectionAdmin)

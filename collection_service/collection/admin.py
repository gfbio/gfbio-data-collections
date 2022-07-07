from django.contrib import admin
from collection_service.collection import models


class CollectionAdmin(admin.ModelAdmin):
    list_filter = ('user_id',)
    search_fields = ['id', 'user_id']
    date_hierarchy = 'created'

    list_display = ('id', 'user_id', 'created')


admin.site.register(models.Collection, CollectionAdmin)

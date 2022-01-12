from django.db import models


class CollectionManager(models.Model):
    #...
    # collection_manager = models.Manager()
    def get_collection(self, collection_id):
        collections = self.filter(broker_submission_id=collection_id)
        if len(collections) == 1:
            return collections.first()
        else:
            return None

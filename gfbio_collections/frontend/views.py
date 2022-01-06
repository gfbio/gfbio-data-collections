from gfbio_collections.collection.models import Collection
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class CollectionsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'pages/home.html'

    def get(self, request):
        queryset = Collection.objects.all()
        return Response({'collections': queryset})

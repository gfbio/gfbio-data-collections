from rest_framework import serializers
from collection_service.collection.models import Collection
from collection_service.collection.utils.schema_validation import validate_json_not_trivial
from collection_service.users.models import Service
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from jsonschema import Draft4Validator


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Positive response',
            value={
                "id": "00c0ffee-c0ff-c0ff-c0ff-c0ffeec0ffee",
                "origin": "gfbio:collection:demoService",
                "set": [
                    {
                        "id": "44233",
                        "name": "Nice sciency data"
                    }
                ],
                "created": "2022-04-07T13:15:17.19",
                "external_user_id": "XY-4999233348",
                "service": 1
            },
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            'Valid request',
            value={
                "set": [
                    {
                        "id": "44233",
                        "name": "Nice sciency data"
                    }
                ],
                "external_user_id": "XY-4999233348"
            },
            request_only=True,
            response_only=False,
        )
    ]
)
class CollectionSerializer(serializers.ModelSerializer):
    origin = serializers.CharField(source='service.origin', read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'external_user_id', 'origin', 'set', 'created', 'service']

    def validate(self, attrs):
        set = attrs['set']
        validate_json_not_trivial(set)

        service = Service.objects.get(pk=attrs['service'])
        schema = service.validation_schema
        if schema:
            validator = Draft4Validator(schema)
            if not validator.is_valid(set):
                error_message = self.collect_validation_errors(set, validator)
                raise serializers.ValidationError(error_message)

        return super().validate(attrs)

    @staticmethod
    def collect_validation_errors(data, validator):
        return [
            '{} : {}'.format(
                error.relative_path.pop() if len(error.relative_path) else '',
                error.message.replace('u\'', '\''))
            for error in validator.iter_errors(data)
        ]

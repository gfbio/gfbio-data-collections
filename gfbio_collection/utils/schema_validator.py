from django.conf import settings
import datetime
import json
import logging
import os

from django.conf import settings
from django.forms import ValidationError
from jsonschema.validators import Draft3Validator, Draft4Validator
from jsonschema import validate, ValidationError, SchemaError

from gfbio_collection.collection.configuration.settings import STATIC_GENERIC_REQUIREMENTS_LOCATION

class CollectionValidator(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def _validate_json(self, json_file, schema):
        """
        """
        try:
            validate(json_file, schema)
        except ValidationError as e:
            raise Exception('Element: %s. Error: %s. ' % (e.path[0], e.message))
        except SchemaError as e:
            raise Exception('Json-schema error:' + e.message)

    def validate_data(self, data={}, schema_file=None, schema_string='{}', use_draft04_validator=False):
        """
        """
        schema_file = os.path.join(settings.STATICFILES_DIRS[0],STATIC_GENERIC_REQUIREMENTS_LOCATION)

        if schema_file:
            with open(schema_file, 'r') as schema:
                schema = json.load(schema)
        else:
            schema = json.loads(schema_string)
        if use_draft04_validator:
            validator = Draft4Validator(schema)
        else:
            validator = Draft3Validator(schema)
        data_valid = validator.is_valid(data)
        errors = [] if data_valid else self.collect_validation_errors(data, validator)
        return data_valid, errors


    def collect_validation_errors(self, data, validator):
        """
        """
        return [
            ValidationError('{} : {}'.format(
                error.relative_path.pop() if len(error.relative_path) else '',
                error.message.replace('u\'', '\''))
            ) for error in validator.iter_errors(data)
        ]

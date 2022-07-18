import re
from rest_framework import serializers


def validate_origin_format(origin):
    if not re.match(r"^[\w\d\_]+(\.[\w\d\_]+)*$", origin):
        raise serializers.ValidationError(
            "The origin needs to consist of namespaces (letters, numbers, undescores),"
            + " optionally separated by dots.")


def validate_json_not_trivial(json):
    if not isinstance(json, (dict, list)):
        type_name = type(json).__name__
        error_message = "The set is '{}', but it needs to be given as list or dictionary.".format(type_name)
        raise serializers.ValidationError(error_message)
    if len(json) < 1:
        raise serializers.ValidationError("The given set is empty.")

import json


def validate_json_string_has_keys(json_str, keys):
    try:
        json_data = json.loads(json_str)
        return validate_json_has_keys(json_data, keys)
    except json.JSONDecodeError:
        return False


def validate_json_has_keys(json_data, keys):
    for key in keys:
        if key not in json_data:
            return False
    return True


def validate_json_string_data(json_str, keys):
    try:
        json_data = json.loads(json_str)
        return validate_json_data(json_data, keys)
    except json.JSONDecodeError:
        return None


def validate_json_data(json_data, keys):
    for key in keys:
        if key not in json_data:
            return None
    return {key: json_data[key] for key in keys}

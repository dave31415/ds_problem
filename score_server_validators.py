from flask import Response

# base error response message
response_400 = "Request not valid, "


def is_request_valid(request):
    if request.headers['Content-Type'] != 'application/json':
        return False, Response(
            response_400 + "Content type should be application/json.", 400)

    data = request.json
    if data is None:
        return False, Response(response_400 + "Missing request body", 400)

    valid, invalid_reason = validate_data(data)
    if not valid:
        return False, Response(response_400 + invalid_reason, 400)

    return True, None


def validate_data(data):
    if not isinstance(data, list):
        return False, "Json data is not a list"

    expected_keys = set("city first_name last_name street "
                        "state amount address_num".split())

    for element in data:
        if not isinstance(element, dict):
            return False, "Some list elements are not dictionaries"
        if not expected_keys.issubset(set(element.keys())):
            return False, "Some list elements missing required fields"
        if not element['amount'].isdigit():
            return False, "Some list elements amount values are not numeric"

    return True, 'OK'

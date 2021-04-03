from functools import wraps

from flask import request
from flask_restful import abort

from api.status_messages import STATUS_400


def validate_request_data(schema, partial):

    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.json:
                abort(400, message=STATUS_400)

            request_data = request.get_json()
            data_errors = schema.validate(request_data, partial=partial)
            if data_errors:
                abort(400, message=data_errors)

            return f(*args, **kwargs)
        return wrapper
    return inner_function

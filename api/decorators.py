from functools import wraps

from flask import request
from flask_restful import abort


def validate_request_data(schema, partial):

    def inner_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.json:
                request_data = request.get_json()
                data_errors = schema.validate(request_data, partial=partial)
                if data_errors:
                    abort(400, message=data_errors)

            return f(*args, **kwargs)
        return wrapper
    return inner_function

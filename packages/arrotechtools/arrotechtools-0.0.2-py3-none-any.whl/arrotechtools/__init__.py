import json
import re
import os
from functools import wraps
from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity


def raise_error(status, msg):
    return make_response(jsonify({
        "status": "400",
        "message": msg
    }), status)

def is_valid_email(variable):
    """Check if email is a valid mail."""
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+$)",
                variable):
        return True
    return False

def is_valid_password(variable):
    """Check if password is a valid password."""
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", variable):
        return True
    return False


def admin_required(users):
    """This is a function.

    Args:
        users (dictionary): Return a array of user objects. A list of users in an array.

    Returns:
        json: Returns Json Object with a message if the user is unauthorized.
    """
    @wraps(users)
    def admin_rights(func):
        """This is a function.

        Args:
            func (function): The function takes another function as an argument.

        Returns:
            function: returns_rights function.
        """
        @wraps(func)
        def wrapper_function(*args, **kwargs):
            """Interface to adapt to the existing codes, so as to save one from modifying thier codes back and forth. 

            Returns:
                function: Returns a function(func) that takes positional and key word arguments.
            """
            try:
                cur_user = [
                    user for user in users if user['email'] == get_jwt_identity()]
                user_role = cur_user[0]['role']
                if user_role != 'admin':
                    return {
                        'message': 'This activity can only be completed by the admin'}, 403  # Forbidden
                return func(*args, **kwargs)
            except Exception as e:
                return {"message": e}

        return wrapper_function
    return admin_rights

"""Decorators used to enforce API authentication and authorization."""

import functools
from .models.TACACS_Auth import TACACS_Auth
from flask import request, Response


def _authenticate_authorize_check(request):
    """Utility function to check for authentication and authorizaton status."""
    # Verify authorization information sent
    if not request.authorization:
        return False, None

    # Perform Authenticaiton and Authorization Checks
    tacacs = TACACS_Auth()
    authenticate = tacacs.authenticate(request.authorization["username"], request.authorization["password"])
    if authenticate:
        rights = tacacs.authorize(request.authorization["username"])
        return True, rights
    else:
        return False, None


def read_required(view):
    """Decorator to require read rights for API or return 403."""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # Check authentication and application rights
        authentication, rights = _authenticate_authorize_check(request)
        if not authentication:
            return Response(status=401)

        # Check for required right
        if not rights.read:
            return Response(status=403)

        return view(*args, **kwargs)

    return wrapped_view


def submit_required(view):
    """Decorator to require read rights for API or return 403."""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # Check authentication and application rights
        authentication, rights = _authenticate_authorize_check(request)
        if not authentication:
            return Response(status=401)

        # Check for required right
        if not rights.submit:
            return Response(status=403)

        return view(*args, **kwargs)

    return wrapped_view


def manage_required(view):
    """Decorator to require read rights for API or return 403."""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # Check authentication and application rights
        authentication, rights = _authenticate_authorize_check(request)
        if not authentication:
            return Response(status=401)

        # Check for required right
        if not rights.manage:
            return Response(status=403)

        return view(*args, **kwargs)

    return wrapped_view

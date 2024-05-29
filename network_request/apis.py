"""Add REST API functionality to the Network-Request Application."""

import functools  # Used to create Decorators for Views

# Import Flask and Flask-RESTx Objects
from flask import Blueprint, request, Response
from flask_restx import Resource, Api

# Import Python libraries and resources required
from dataclasses import asdict, fields
from uuid import uuid4

# Import elements of the Network-Request Application
from network_request.services import service_list  # The list of Services created
from .models.VLAN_Service import VLAN_Service  # Class representing a VLAN Service
from .api_auth import read_required, submit_required, manage_required  # Decorators for managing authentication


# List of supported authorizations for this API
authorizations = {
    "basic": {
        "type": "basic",
    }
}

# Setup Flask objects
bp = Blueprint("api", __name__)
api = Api(bp, authorizations=authorizations, security="basic")


def verify_payload_fields(view):
    """Decorator to verify fields provided in payload are valid."""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # Create a set of allowed VLAN Service Fields for verifying input
        fields_vlan_service = set([field.name for field in fields(VLAN_Service)])

        # Verify no invalid keys are submitted
        #   This is accomplished with Python set operations be ensuring the keys
        #   in the API body (payload) are contained within the set of allowed fields
        if not fields_vlan_service.issuperset(set(api.payload.keys())):
            return {
                "message": "Payload includes invalid keys.",
                "allowed_keys": list(fields_vlan_service),
            }, 400

        # If a status field was provided, verify it is a valid value
        try:
            if api.payload["status"] not in ["approved", "denied", "submitted"]:
                return {"message": "status must be 'approved' or 'denied'."}, 400
        except KeyError:
            pass

        return view(*args, **kwargs)

    return wrapped_view


# TODO: Serve the API route "/services" with the ServicesList class
class ServicesList(Resource):
    """API Class for interacting with the list of Services."""

    # TODO: Update the lookup method to provide READ access to services
    # TODO: Leverage the available decorators from api_auth to require "read" rights to this API
    def lookup(self):
        """Allow READ access to retrieve all defined Services via API."""
        # Use the asdict funciton from data classes to make each VLAN_Service
        # JSON serializable
        return {uuid: asdict(service) for uuid, service in service_list.items()}

    # TODO: Update the create_new method to provide CREATE access to services
    # TODO: Leverage the available decorators from api_auth to require "submit" rights to this API
    # TODO: Leverage the available function verify_payload_fields to ensure data submitted with the API is valid
    # TODO: Ensure appropriate HTTP status code provided to users when this API is successful
    def create_new(self):
        """Allow CREATE operation to add a new Service via API."""
        new_uuid = uuid4().int
        service_list[new_uuid] = VLAN_Service(
            name=api.payload["name"],
            description=api.payload["description"],
            submitter=request.authorization.username,
        )
        return {"uuid": str(new_uuid)}


# TODO: Provide access to individual Services at the "/services" route when identified by a "uuid" parameter
#       - UUIDs are Python Integers
class Service(Resource):
    """API Class for interacting with a single Service by UUID."""

    # TODO: Update the lookup method to provide READ access to services
    # TODO: Leverage the available decorators from api_auth to require "read" rights to this API
    def lookup(self, uuid):
        """Allow READ access to access details for a specific Service by UUID."""
        # Use the asdict funciton from data classes to make each VLAN_Service
        # JSON serializable
        try:
            service = service_list[uuid]
            return asdict(service)
        # TODO: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response()

    # TODO: Update the replace method to provide UPDATE access to services
    # TODO: Leverage the available decorators from api_auth to require "manage" rights to this API
    # TODO: Leverage the available function verify_payload_fields to ensure data submitted with the API is valid
    # TODO: Ensure appropriate HTTP status code provided to users when this API is successful
    def replace(self, uuid):
        """Allow UPDATE action on an existing Service by replacing Service details."""
        try:
            service = service_list[uuid]
        # TODO: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response()

        # Replace data for the service
        service.status = api.payload["status"]
        service.name = api.payload["name"]
        service.description = api.payload["description"]
        service.id = api.payload["id"]
        service.submitter = api.payload["submitter"]

        return Response()

    # TODO: Update the modify method to provide partial UPDATE access to services
    # TODO: Leverage the available decorators from api_auth to require "manage" rights to this API
    # TODO: Leverage the available function verify_payload_fields to ensure data submitted with the API is valid
    # TODO: Ensure appropriate HTTP status code provided to users when this API is successful
    def modify(self, uuid):
        """Allow UPDATE action on an existing Service by updating provided Service details."""
        try:
            service = service_list[uuid]
        # TODO: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response()

        # Loop over the payload provided and update whichever fields are provided
        for key, value in api.payload.items():
            setattr(service, key, value)

        return Response()

    # TODO: Update the remove method to provide DELETE access to services
    # TODO: Leverage the available decorators from api_auth to require "manage" rights to this API
    # TODO: Ensure appropriate HTTP status code provided to users when this API is successful
    def remove(self, uuid):
        """Allow DELETE action on an existing Service by deleting the provided Service by UUID."""
        try:
            service_list.pop(uuid)
        # TODO: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response()

        return Response()

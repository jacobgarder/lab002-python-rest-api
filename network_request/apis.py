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


# DONE: Serve the API route "/services" with the ServicesList class
@api.route("/services")
class ServicesList(Resource):
    """API Class for interacting with the list of Services."""

    # DONE: Update the lookup method to provide READ access to services
    # DONE: Leverage the available decorators from api_auth to require "read" rights to this API
    @read_required
    def get(self):
        """Allow READ access to retrieve all defined Services via API."""
        # Use the asdict funciton from data classes to make each VLAN_Service
        # JSON serializable
        return {uuid: asdict(service) for uuid, service in service_list.items()}

    # DONE: Update the create_new method to provide CREATE access to services
    # DONE: Leverage the available decorators from api_auth to require "submit" rights to this API
    # DONE: Leverage the available function verify_payload_fields to ensure data submitted with the API is valid
    # DONE: Ensure appropriate HTTP status code provided to users when this API is successful
    @submit_required
    @verify_payload_fields
    def post(self):
        """Allow CREATE operation to add a new Service via API."""
        new_uuid = uuid4().int
        service_list[new_uuid] = VLAN_Service(
            name=api.payload["name"],
            description=api.payload["description"],
            submitter=request.authorization.username,
        )
        return {"uuid": str(new_uuid)}, 201


# DONE: Provide access to individual Services at the "/services" route when identified by a "uuid" parameter
#       - UUIDs are Python Integers
@api.route("/services/<int:uuid>")
@api.param("uuid", "The Service UUID")
class Service(Resource):
    """API Class for interacting with a single Service by UUID."""

    # DONE: Update the lookup method to provide READ access to services
    # DONE: Leverage the available decorators from api_auth to require "read" rights to this API
    @read_required
    def get(self, uuid):
        """Allow READ access to access details for a specific Service by UUID."""
        # Use the asdict funciton from data classes to make each VLAN_Service
        # JSON serializable
        try:
            service = service_list[uuid]
            return asdict(service)
        # DONE: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response(status=404)

    # DONE: Update the replace method to provide UPDATE access to services
    # DONE: Leverage the available decorators from api_auth to require "manage" rights to this API
    # DONE: Leverage the available function verify_payload_fields to ensure data submitted with the API is valid
    # DONE: Ensure appropriate HTTP status code provided to users when this API is successful
    @manage_required
    @verify_payload_fields
    def put(self, uuid):
        """Allow UPDATE action on an existing Service by replacing Service details."""
        try:
            service = service_list[uuid]
        # TODO: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response(status=404)

        # Replace data for the service
        service.status = api.payload["status"]
        service.name = api.payload["name"]
        service.description = api.payload["description"]
        service.id = api.payload["id"]
        service.submitter = api.payload["submitter"]

        return Response(status=204)

    # DONE: Update the modify method to provide partial UPDATE access to services
    # DONE: Leverage the available decorators from api_auth to require "manage" rights to this API
    # DONE: Leverage the available function verify_payload_fields to ensure data submitted with the API is valid
    # DONE: Ensure appropriate HTTP status code provided to users when this API is successful
    @manage_required
    @verify_payload_fields
    def patch(self, uuid):
        """Allow UPDATE action on an existing Service by updating provided Service details."""
        try:
            service = service_list[uuid]
        # DONE: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response(status=404)

        # Loop over the payload provided and update whichever fields are provided
        for key, value in api.payload.items():
            setattr(service, key, value)

        return Response(status=204)

    # DONE: Update the remove method to provide DELETE access to services
    # DONE: Leverage the available decorators from api_auth to require "manage" rights to this API
    # DONE: Ensure appropriate HTTP status code provided to users when this API is successful
    @manage_required
    def delete(self, uuid):
        """Allow DELETE action on an existing Service by deleting the provided Service by UUID."""
        try:
            service_list.pop(uuid)
        # DONE: Ensure appropriate HTTP status code provided to users if the provided UUID isn't found
        except KeyError:
            return Response(status=404)

        return Response(status=204)

from dataclasses import dataclass
from typing import Optional

# from tacacs_plus.client import TACACSClient
# from tacacs_plus.flags import TAC_PLUS_ACCT_FLAG_START

from .App_Rights import App_Rights

import os
import logging

# For the DevNet Expert Practice Lab, the full TACACS server is removed from
# the demo. This model has been updated to offer simple RBAC services with
# minimal code changes from original application.
users = {
    "sysadmin": {
        "password": "password",
        "rights": {
            "read": "allow",
            "submit": "allow",
            "manage": "allow",
        },
    },
    "customer": {
        "password": "password",
        "rights": {
            "read": "reject",
            "submit": "allow",
            "manage": "reject",
        },
    },
    "operator": {
        "password": "password",
        "rights": {
            "read": "allow",
            "submit": "allow",
            "manage": "reject",
        },
    },
}


@dataclass
class TACACS_Auth:
    server: Optional[str] = os.getenv("TACACS_HOST")
    secret_key: Optional[str] = os.getenv("TACACS_SECRET")
    tacacs_port: Optional[int] = 49
    application_name: Optional[str] = os.getenv("TACACS_APP_NAME", "python application")
    aaa_port: Optional[str] = "python_tacacs"
    # client: Optional[TACACSClient] = TACACSClient(
    #     host=server, port=tacacs_port, secret=secret_key, timeout=10
    # )

    @staticmethod
    def authorization_args_to_dict(arguments: list) -> dict[str, str]:
        """Return an AV Pairs Dictionary of arguments"""
        av_pairs = {}
        for argument in arguments:
            # Convert bytes to stgring
            argument = argument.decode("utf-8")
            # Note: Is there any time when an argument might have more than one "="?
            key, value = argument.split("=")
            av_pairs[key] = value
        return av_pairs

    def authenticate(self, username: str, password: str) -> bool:
        """Perform a TACACS Authentication"""

        logging.info(f"Sending TACACS authenticate request for username [{username}] ")
        # result = self.client.authenticate(
        #     username=username,
        #     password=password,
        #     rem_addr=self.application_name,
        #     port=self.aaa_port,
        # )
        # logging.info(f"Result: {result.valid}")
        if username in users.keys():
            if users[username]["password"] == password:
                return True

        return False

    def authorize(self, username: str) -> App_Rights:
        """Perform a TACACS Authorization to determine permissions for user"""

        rights_mapping = {"allow": True, "reject": False}

        logging.info(f"Sending TACACS authorization request for username [{username}]")
        # result = self.client.authorize(
        #     username=username,
        #     arguments=[b"service=rights"],
        #     rem_addr=self.application_name,
        #     port=self.aaa_port,
        # )
        # logging.info(f"Result: {result.valid}")
        # if not result.valid:
        #     logging.error(f"ERROR: Attempt to Authorize username [{username}] failed.")
        #     return None

        # logging.debug(f"TACACS Authorization Arguments: {result.arguments}")
        # rights = TACACS_Auth.authorization_args_to_dict(result.arguments)

        rights = users[username]["rights"]

        logging.info(f"Rights for [{username}] are {rights}")

        app_rights = App_Rights(
            read=rights_mapping[rights["read"]],
            submit=rights_mapping[rights["submit"]],
            manage=rights_mapping[rights["manage"]],
        )

        return app_rights

    def accounting(self, username: str, action: str, message: str) -> bool:
        """Record an accounting message"""

        logging.info(
            f"Sending a TACACS accounting request for username [{username}] action [{action}] message [{message}]"
        )
        # result = self.client.account(
        #     username=username,
        #     flags=TAC_PLUS_ACCT_FLAG_START,
        #     arguments=[
        #         str.encode(f"service={action}"),
        #         str.encode(f"message={message}"),
        #     ],
        #     rem_addr=self.application_name,
        #     port=self.aaa_port,
        # )
        # logging.info(f"Result: {result.valid}")
        return True

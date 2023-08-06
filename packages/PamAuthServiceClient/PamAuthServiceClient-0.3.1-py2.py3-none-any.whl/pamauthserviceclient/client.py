import json
import logging
import time
from base64 import urlsafe_b64decode
from urllib.parse import quote_plus

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import ed25519
from jsonschema import validate

logger = logging.getLogger(__name__)

response_schema = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": ["version", "username", "allowed_groups"],
    "additionalProperties": False,
    "properties": {
        "version": {
            "$id": "#/properties/version",
            "type": "string",
            "title": "The Version Schema",
            "default": "1.0",
            "pattern": "^1.0$",
        },
        "username": {
            "$id": "#/properties/username",
            "type": "string",
            "title": "Username",
            "minLength": 1,
            "maxLength": 256,
        },
        "allowed_groups": {
            "$id": "#/properties/allowed_groups",
            "type": "array",
            "title": "List of groups, the user could be member of",
            "items": {
                "$id": "#/properties/groups/items",
                "type": "string",
                "title": "name of a group",
                "minLength": 1,
                "maxLength": 256,
            },
        },
    },
}


class PamAuthServiceClient:
    """
    A client for the PamAuthService
    """

    def __init__(self, encryption_key, verification_key, *, path=None, url=None):
        """
        Initialize the Client

        :param encryption_key: A key for a FERNET encryption.
               This key will be used to encrypt the authorization request
               (which includes a cleartext password)
        :param verification_key: A key to verify a signature with an
               elliptic curve algorithm. This key will be used to
               verify the authenticity of the response.
        :param url: The base url for the PamAuthService, if it is available
               via a network socket. (i.e.: "http://127.0.0.1:5000")
        :param path: The path to the unix-socket for the PamAuthService,
               if it is available via unix-sockets.
               (i.e.: "/run/pam_auth_service.sock")
        """
        self.encryption = Fernet(encryption_key)
        public_bytes = urlsafe_b64decode(verification_key.encode())
        self.verification = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
        if path is None and url is None:
            raise AttributeError(
                "You have to set either a 'path' or an 'url' to the PamAuthService."
            )
        if path is not None and url is not None:
            raise AttributeError("You can't set both 'path' and 'url'.")
        if url:
            import requests

            self.requests = requests
            self.base_url = url
        else:
            import requests_unixsocket

            self.requests = requests_unixsocket
            self.base_url = f"http+unix://{quote_plus(path, safe='')}"

    @staticmethod
    def _verify_parameters(username, password, groups):
        """
        Helper function to verify the format of the parameters

        :param username: The login name of the user as a string
        :param password: The password of the user as a string
        :param groups:  A list of group names as a string
        """
        if not isinstance(username, str):
            raise ValueError("username is not a string")
        if not isinstance(password, str):
            raise ValueError("password is not a string")
        if not isinstance(groups, list):
            raise ValueError("group is not a list")
        for group in groups:
            if not isinstance(group, str):
                raise ValueError("An element of groups is not a string")

    def authenticate(self, username, password, allowed_groups=None):
        """
        Authenticate a user with the service

        :param username: The login name
        :param password: The password of the user
        :param allowed_groups: A list of group names. (optional)
               If the user is authenticated then it will be checked if
               the user is a member of any of this groups. The names
               of the groups in this list of which the user is a member
               of will be returned. **The user is still authenticated,
               even if he is no member of any groups in this list or if
               the list isn't set at all or if it is empty!**
        :return: `None` if the user is not authenticated or a dict of
               the form as described as in the `response_schema`.
        """
        if allowed_groups is None:
            allowed_groups = []

        self._verify_parameters(username, password, allowed_groups)

        request_payload = {
            "version": "1.0",
            "username": username,
            "password": password,
            "allowed_groups": allowed_groups,
        }
        try:
            token = self._encrypt_payload(request_payload)
            response = self.requests.post(self.base_url + "/authorize", data=token)
            response.raise_for_status()

            response_payload = self._verify_response(username, response)
            return response_payload
        except Exception as err:
            logger.error(f"{repr(err)}")
            return None

    def _verify_response(self, username, response):
        """
        Helper method to verify the signature of the response
        :param username: Name of the user for the requested authentication
        :param response: Response to the request
        :return: a dict with the response data
        """

        b64_payload, b64_signature = response.text.split(".")
        response_json_payload = urlsafe_b64decode(b64_payload.encode())
        signature = urlsafe_b64decode(b64_signature.encode())
        self.verification.verify(signature, response_json_payload)
        response_payload = json.loads(response_json_payload.decode())
        validate(response_schema, response_payload)
        if response_payload["username"] != username:
            raise ValueError("username in response doesn't match request username")
        return response_payload

    def _encrypt_payload(self, payload):
        """
        Helper method to encrypt the payload

        :param payload: dict with the request data
        :return: encrypted payload
        """
        json_payload = json.dumps(payload).encode()
        token = self.encryption.encrypt_at_time(json_payload, int(time.time()))
        return token

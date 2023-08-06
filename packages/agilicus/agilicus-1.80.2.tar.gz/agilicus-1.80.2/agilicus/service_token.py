from datetime import datetime
from datetime import timedelta
from datetime import timezone
import jwt
import json

from . import tokens
import agilicus
import agilicus_api


class Token:
    """Class for managing token lifecycle for service accounts."""

    def __init__(
        self=None,
        org_id=None,
        user_id=None,
        auth_issuer_url=None,
        auth_expiry_secs=86400,
        access_token=None,
        scope=None,
        api_host=None,
        cacert=None,
        client_id=None,
        referer=None,
        auth_doc=None,
        **kwargs,
    ):
        self.org_id = org_id
        self.user_id = user_id
        self.auth_issuer_url = auth_issuer_url
        self.auth_expiry_secs = auth_expiry_secs
        self.configuration = agilicus.Configuration()
        self.configuration.access_token = access_token
        self.configuration.host = api_host
        if not api_host:
            self.configuration.host = "https://api.agilicus.com"
        self.configuration.ssl_ca_cert = cacert
        self.tokens_api = agilicus_api.TokensApi(agilicus.ApiClient(self.configuration))

        self.client_id = client_id
        self.referer = referer
        self.scope = scope
        self.token = None
        self.auth_doc = auth_doc
        self.auth_doc_static = False
        if auth_doc:
            # the auth doc is not requested.
            self.auth_doc_static = True

    def is_expired(self):
        if not self.token:
            return True
        if datetime.now(timezone.utc) > self.token_expiry:
            return True

    def set_access_token(self, token):
        self.configuration.access_token = token

    def get_auth_document_expiry(self):
        if self.auth_doc:
            if self.auth_doc["spec"]["expiry"]:
                return datetime.fromisoformat(self.auth_doc["spec"]["expiry"])

    def get_auth_document(self):
        if self.auth_doc:
            if self.auth_doc["spec"]["expiry"]:
                expiry = datetime.fromisoformat(self.auth_doc["spec"]["expiry"])
                if datetime.now(timezone.utc) < expiry:
                    return self.auth_doc

        if self.auth_doc_static:
            raise ("Static authentication document has expired")

        auth_expiry = str(
            datetime.now(timezone.utc) + timedelta(seconds=self.auth_expiry_secs)
        )

        spec = agilicus_api.AuthenticationDocumentSpec(
            org_id=self.org_id,
            user_id=self.user_id,
            auth_issuer_url=self.auth_issuer_url,
            expiry=auth_expiry,
        )
        model = agilicus_api.AuthenticationDocument(spec=spec)
        self.auth_doc = self.tokens_api.create_authentication_document(model).to_dict()
        return self.auth_doc

    def get(self):
        if self.is_expired():
            _token = tokens.create_service_token(
                self.get_auth_document(),
                verify=self.configuration.ssl_ca_cert,
                scope=self.scope,
                client_id=self.client_id,
                referer=self.referer,
            )
            _token = json.loads(_token)
            self.token = _token["access_token"]
            _token_dict = jwt.decode(self.token, verify=False)
            _exp = datetime.fromtimestamp(_token_dict["exp"], tz=timezone.utc)
            _iat = datetime.fromtimestamp(_token_dict["iat"], tz=timezone.utc)
            # grab a new token when expiry is half expired
            self.token_expiry = _iat + ((_exp - _iat) / 2)
        return self.token

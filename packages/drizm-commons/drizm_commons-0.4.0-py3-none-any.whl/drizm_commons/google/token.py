import requests
import requests.adapters
import google.auth.exceptions
from google.oauth2 import service_account
from google.oauth2._client import id_token_jwt_grant  # noqa protected
from google.auth.transport.requests import Request


def construct_service_authentication_request() -> Request:
    auth_request_session = requests.Session()
    retry_adapter = requests.adapters.HTTPAdapter(max_retries=3)
    auth_request_session.mount("https://", retry_adapter)
    auth_request = Request(auth_request_session)
    return auth_request


def force_obtain_id_token(credentials: service_account.IDTokenCredentials) -> str:
    """ Manually forces the equivalent of credentials.refresh() """
    assertion = credentials._make_authorization_grant_assertion()  # noqa protected
    request = construct_service_authentication_request()
    try:
        access_token, *_ = id_token_jwt_grant(
            request,
            credentials._token_uri,  # noqa protected
            assertion  # noqa expected type
        )
    except google.auth.exceptions.RefreshError as exc:
        raise Exception(
            "Error when requesting the token, "
            "you may have provided an empty target_audience parameter,"
            " for the Credentials object."
        ) from exc
    return access_token

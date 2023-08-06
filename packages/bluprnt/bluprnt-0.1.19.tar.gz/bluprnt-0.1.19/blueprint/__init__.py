import logging
import os
import json
from base64 import urlsafe_b64decode
import requests
from requests.exceptions import HTTPError
from flask import Request, jsonify
from google.cloud import tasks


SERVICE_CATALOG = json.loads(os.environ["SERVICE_CATALOG"])
QUEUE_CATALOG = json.loads(os.environ["QUEUE_CATALOG"])
TASKS = tasks.CloudTasksClient()


def get_service_account_metadata(field, params=None):
    url = (
        "http://metadata.google.internal"
        f"/computeMetadata/v1/instance/service-accounts/default/{field}"
    )
    return requests.get(
        url=url, headers={"Metadata-Flavor": "Google"}, params=params
    ).content.decode()


def get_service_url(service_name, service_path=None):
    url = SERVICE_CATALOG.get(service_name)
    if not url:
        raise Exception(f"Service '{service_name}' not found in catalog.")
    if service_path:
        url += f"/{service_path}"
    return url


def call(service_name, service_path=None, **kwargs):
    url = get_service_url(service_name, service_path)
    auth = {
        "Authorization": "Bearer "
        + get_service_account_metadata("identity", {"audience": url})
    }
    r = requests.post(url, headers=auth, json=kwargs)
    if r.status_code >= 500:
        r.raise_for_status()
    return r


def queue(calls):
    scheduled = []
    for call in calls:
        service_name = call["service_name"]
        service_path = call["service_path"]
        data = call["data"]
        task = TASKS.create_task(
            parent=QUEUE_CATALOG[service_name],
            task=tasks.Task(
                http_request=tasks.HttpRequest(
                    http_method=tasks.HttpMethod.POST,
                    url=get_service_url(service_name, service_path),
                    body=json.dumps(data).encode(),
                    oidc_token=tasks.OidcToken(
                        service_account_email=get_service_account_metadata("email")
                    ),
                )
            ),
        )
        scheduled.append(task)
    return scheduled


def user_info(request: Request):
    encoded_user_info = request.headers.get("X-Endpoint-Api-Userinfo")
    if encoded_user_info:
        if not encoded_user_info.endswith("=="):
            encoded_user_info += "=="
        return json.loads(urlsafe_b64decode(encoded_user_info))
    return {}


def handle_http_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            logging.exception(e.response.content.decode())
        except Exception as e:
            logging.exception(e)
        return (
            jsonify(message="An unexpected error occurred."),
            500,
        )

    return wrapper


def validate(**kwargs):
    def wrap(func):
        def wrapper(request: Request):
            try:
                for key in kwargs:
                    valid = kwargs[key](request.json.get(key))
                    if not valid:
                        return (
                            jsonify(message=f"Invalid value for '{key}'"),
                            400,
                        )
            except Exception as e:
                logging.exception(e)
                return (
                    jsonify(message="An unexpected error occurred in validation."),
                    500,
                )
            return func(request)

        return wrapper

    return wrap


def auth(permission):
    def wrap(func):
        def wrapper(request: Request):
            try:
                if not "asset" in request.json:
                    return (
                        jsonify(
                            message="Missing required 'asset' parameter in authorized request."
                        ),
                        400,
                    )
                r = call(
                    "db",
                    "authorize",
                    asset=request.json["asset"],
                    uid=user_info(request)["user_id"],
                    permission=permission,
                )
                r.raise_for_status()
                if not r.json()["granted"]:
                    return jsonify(message="Access denied."), 403
            except Exception as e:
                logging.exception(e)
                return (
                    jsonify(message="An unexpected error occurred in authorization."),
                    500,
                )
            return func(request)

        return wrapper

    return wrap


def _trim_document_path(path):
    return "/".join(path.split("/")[5:])


class Asset:
    def __init__(self, path):
        self.path = path
        path_parts = self.path.split("/")
        self.id = path_parts[-1]
        self.type = path_parts[-2]
        if len(path_parts) > 2:
            self.parent = Asset("/".join(path_parts[:-2]))
        else:
            self.parent = None


class ParsedRequest:
    def __init__(self, request: Request):
        self.data = request.json
        self.user_info = user_info(request)
        self.asset = Asset(self.data["asset"]) if "asset" in self.data else None


class DBEvent:
    def __init__(self, event):
        value = event["value"] or event["oldValue"]
        self.asset = Asset(_trim_document_path(value["name"]))
        self.data = self._raise_values(value["fields"])

    def _raise_value(self, value_obj):
        value_type = next(iter(value_obj))
        if value_type == "mapValue":
            value = self._raise_values(value_obj[value_type])
        elif value_type == "arrayValue":
            value = [self._raise_value(v) for v in value_obj[value_type]["values"]]
        elif value_type == "referenceValue":
            value = Asset(_trim_document_path(value_obj[value_type]))
        else:
            value = value_obj[value_type]
        return value

    def _raise_values(self, fields):
        values = {}
        for key in fields:
            values[key] = self._raise_value(fields[key])
        return values

"""SDC2 scoring service API functions."""
import os
import json
import http.client
from http import HTTPStatus
import urllib.parse
import logging
from keycloak import KeycloakOpenID
from requests.models import encode_multipart_formdata
import requests


LOG = logging.getLogger(__name__)

SDC_SCORE_API_HOST = os.getenv("SDC_SCORE_API_HOST", "130.246.212.180")
SDC_SCORE_API_PORT = os.getenv("SDC_SCORE_API_PORT", "3000")
SDC_SCORE_AUTH_HOST = os.getenv("SDC_SCORE_AUTH_HOST", "130.246.212.32")
SDC_SCORE_AUTH_PORT = os.getenv("SDC_SCORE_AUTH_PORT", "8080")
SDC_SCORE_AUTH_CLIENT_ID = "sdc"
SDC_SCORE_AUTH_REALM_NAME = "sdc"


def get_token(username: str, password: str):
    """Get keyclock token."""
    auth_url = f"http://{SDC_SCORE_AUTH_HOST}:{SDC_SCORE_AUTH_PORT}/auth/"
    LOG.debug(f"Auth url = {auth_url}")
    LOG.debug(f"Getting auth token... {username} - {password}")
    keycloak_openid = KeycloakOpenID(
        auth_url,
        client_id=SDC_SCORE_AUTH_CLIENT_ID,
        realm_name=SDC_SCORE_AUTH_REALM_NAME,
    )
    token = keycloak_openid.token(username=username, password=password)
    return token


def get_config(endpoint: str):
    """Return json configuration data at specified endpoint."""
    conn = http.client.HTTPConnection(SDC_SCORE_API_HOST, SDC_SCORE_API_PORT)
    conn.request("GET", endpoint)
    resp = conn.getresponse()
    LOG.debug("%s %s", resp.status, resp.reason)
    data = resp.read().decode("utf-8")
    conn.close()
    return json.loads(data)


def get_user_uuid(username: str):
    """Return the user uuid for a specified username."""
    users = get_config("/users")
    try:
        uuid = next(user[0] for user in users if user[3] == username)
        return uuid
    except StopIteration:
        return None


def display_leaderboard():
    """Display the leaderboard."""
    leaderboard = get_config("/sdc2/leaderboard")
    LOG.info("Leaderboard:")
    for score in leaderboard:
        LOG.info(score)


def create_submission(username, password, catalogue_file):
    """Create submision."""
    LOG.info("Authenticating as user: %s", username)
    auth_token = get_token(username, password)
    LOG.info("Creating submission from file: %s", catalogue_file)
    headers = {"Authorization": "Bearer " + auth_token["access_token"]}
    files = {
        "submissionFile": (
            catalogue_file,
            open(catalogue_file, "rb"),
            "text/plain",
        )
    }
    params = urllib.parse.urlencode(
        {
            "subSkipRows": 0,
            "truthSkipRows": 0,
        }
    )
    url = f"http://{SDC_SCORE_API_HOST}:{SDC_SCORE_API_PORT}"
    url += "/sdc2/v1/submission"
    url += "?" + params
    resp = requests.post(url, files=files, headers=headers, timeout=10)
    if resp.status_code == HTTPStatus.OK.value:
        LOG.info("Submission sucessful!")
        LOG.info("Submission id: %s", resp.text)
        LOG.info("(Please take a note of this as it is needed to check the status!)")
    else:
        LOG.error("Failed to create submission. %s : %s", resp.status_code, resp.text)


def display_submission_status(submisson_uuid: str):
    """Get the submission status."""
    LOG.info("Getting submission status: %s", submisson_uuid)
    conn = http.client.HTTPConnection(SDC_SCORE_API_HOST, SDC_SCORE_API_PORT)
    params = urllib.parse.urlencode({"submissionId": submisson_uuid})
    conn.request("GET", "/sdc2/v1/submission" + "?" + params)
    resp = conn.getresponse()
    if resp.status != HTTPStatus.OK:
        LOG.error("Failed to get status. %s : %s", resp.status, resp.reason)
    data = json.loads(resp.read().decode("utf-8"))
    conn.close()
    LOG.info("Status = %s (%s)", data[5], data[4])

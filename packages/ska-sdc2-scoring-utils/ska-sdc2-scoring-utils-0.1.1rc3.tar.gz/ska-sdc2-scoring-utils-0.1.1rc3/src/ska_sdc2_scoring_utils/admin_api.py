"""SDC2 scoring service admin API functions."""
import os
import sys
import json
import http.client
from http import HTTPStatus
import urllib.parse
import logging
from keycloak import KeycloakOpenID

LOG = logging.getLogger(__name__)

SDC_SCORE_API_HOST = os.getenv("SDC_SCORE_API_HOST", "130.246.212.180")
SDC_SCORE_API_PORT = os.getenv("SDC_SCORE_API_PORT", "3000")
SDC_SCORE_AUTH_HOST = os.getenv("SDC_SCORE_AUTH_HOST", "130.246.212.32")
SDC_SCORE_AUTH_PORT = os.getenv("SDC_SCORE_AUTH_PORT", "8080")
SDC_SCORE_AUTH_CLIENT_ID = "sdc"
SDC_SCORE_AUTH_REALM_NAME = "sdc"


def get_admin_token():
    """Get keyclock admin token."""
    user = os.getenv("SDC2_SCORER_ADMIN_USER", None)
    passwd = os.getenv("SDC2_SCORER_ADMIN_PASSWORD", None)
    if not user or not passwd:
        LOG.error(
            "In order to use this app, please set the env varaibles: SDC2_SCORER_ADMIN_USER and SDC2_SCORER_ADMIN_PASSWORD"
        )
        sys.exit(1)
    auth_url = f"http://{SDC_SCORE_AUTH_HOST}:{SDC_SCORE_AUTH_PORT}/auth/"
    LOG.debug(f"auth url = {auth_url}")
    LOG.debug(f"getting auth token... {user} - {passwd}")
    keycloak_openid = KeycloakOpenID(
        auth_url,
        client_id=SDC_SCORE_AUTH_CLIENT_ID,
        realm_name=SDC_SCORE_AUTH_REALM_NAME,
    )
    token = keycloak_openid.token(username=user, password=passwd)
    return token


def get_config(endpoint):
    """Return json configuration data at specified endpoint."""
    token = get_admin_token()
    conn = http.client.HTTPConnection(SDC_SCORE_API_HOST, SDC_SCORE_API_PORT)
    _headers = {"Authorization": "Bearer " + token["access_token"]}
    conn.request("GET", endpoint, headers=_headers)
    resp = conn.getresponse()
    LOG.debug("%s %s", resp.status, resp.reason)
    data = resp.read().decode("utf-8")
    conn.close()
    return json.loads(data)


def get_users_group(user_group_uuid):
    """Return group for specified user."""
    groups = get_config("/groups")
    try:
        group = next(
            group_data for group_data in groups if group_data[0] == user_group_uuid
        )
        return group[1]
    except StopIteration:
        return None


def get_group_uuid(group_name):
    """Return the group uuid for a specified group name."""
    groups = get_config("/groups")
    try:
        uuid = next(
            group_data[0] for group_data in groups if group_data[1] == group_name
        )
        return uuid
    except StopIteration:
        return None


def get_group_name(group_uuid):
    """Return the group name for a specified group uuid."""
    groups = get_config("/groups")
    try:
        name = next(group[1] for group in groups if group[0] == group_uuid)
        return name
    except StopIteration:
        return None


def get_user_uuid(username: str):
    """Return the user uuid for a specified username."""
    users = get_config("/users")
    try:
        uuid = next(user[0] for user in users if user[3] == username)
        return uuid
    except StopIteration:
        return None


def get_users_in_group(group_uuid: str):
    """Return the user uuid for a specified username."""
    all_users = get_config("/users")
    group_users = []
    for user in all_users:
        if user[5] == group_uuid:
            group_users.append(user)
    return group_users


# =============================================================================
# GROUP methods
# =============================================================================


def user_list():
    """Display list of users."""
    LOG.info("Users: <Last Name, First Name | username | email | uuid | group name>")
    for user in get_config("/users"):
        # LOG.info(f"   {user}")
        group = get_users_group(user[5])
        LOG.info(
            f"   {user[2]}, {user[1]} | {user[3]} | {user[4]} | {user[0]} | {group}"
        )


def user_add(
    first_name: str,
    last_name: str,
    username: str,
    password: str,
    email: str,
    group_name: str = None,
):
    """Add a new user.

    Args:
        first_name (str):
        last_name (str):
        username (str):
        password (str):
        email (str):
        group_name (str):

    TODO:
        - Dont allow adding two users with the same name!
    """
    LOG.info(
        "Adding user: %s %s (%s) | password: '%s'",
        first_name,
        last_name,
        username,
        password,
    )
    group_name = " ".join(group_name)
    group_uuid = get_group_uuid(group_name)
    if not group_uuid:
        LOG.error("Unable to add user, group with name '%s' not found!", group_name)
        return

    token = get_admin_token()
    conn = http.client.HTTPConnection(SDC_SCORE_API_HOST, SDC_SCORE_API_PORT)
    headers = {
        "Authorization": "Bearer " + token["access_token"],
        "Content-Type": "multipart/form-data",
        "Accept": "application/json",
    }
    params = urllib.parse.urlencode(
        {
            "firstName": first_name,
            "lastName": last_name,
            "username": username,
            "password": password,
            "email": email,
            "groupId": group_uuid,
        }
    )
    conn.request("POST", "/users" + "?" + params, headers=headers)
    resp = conn.getresponse()
    data = json.loads(resp.read().decode("utf-8"))
    conn.close()
    if resp.status == HTTPStatus.OK:
        LOG.info(
            "Sucessfully added user '%s %s (%s)', uuid = %s",
            first_name,
            last_name,
            username,
            data,
        )
    else:
        LOG.error("Failed to add user. %s : %s (%s)", resp.status, resp.reason, data)


def user_delete(username: str):
    """Delete a user.

    Args:
        username(str): Username

    """
    uuid = get_user_uuid(username)
    if not uuid:
        LOG.error("User id for username '%s' not found!", username)
        return

    LOG.info("Deleteing User: '%s' (%s)", username, uuid)
    token = get_admin_token()
    conn = http.client.HTTPConnection(SDC_SCORE_API_HOST, SDC_SCORE_API_PORT)
    headers = {
        "Authorization": "Bearer " + token["access_token"],
        "Content-Type": "multipart/form-data",
        "Accept": "application/json",
    }
    params = urllib.parse.urlencode({"userId": uuid})
    conn.request("DELETE", "/users" + "?" + params, headers=headers)
    resp = conn.getresponse()
    data = json.loads(resp.read().decode("utf-8"))
    conn.close()
    if resp.status == HTTPStatus.OK:
        LOG.info("Sucessfully deleted user '%s', uuid = %s", username, data)
    else:
        LOG.error(
            "Failed to delete user. '%s' : %s (%s)", resp.status, resp.reason, data
        )


# =============================================================================
# GROUP methods
# =============================================================================


def group_list(show_users=False):
    """Display list of groups."""
    groups = get_config("/groups")
    LOG.info("Groups%s:", " (and users in each group)" if show_users else "")
    for group in groups:
        LOG.info(f"  {group[1]:40s} (group id: {group[0]})")
        if show_users:
            users = get_users_in_group(group_uuid=group[0])
            for user in users:
                LOG.info(f"    {user[1]} {user[2]:40s} (user id: {user[0]})")


def group_add(name: str):
    """Add a new group.

    Args:
        name (str): Name of the group to add.
    """
    name = " ".join(name)
    LOG.info("Adding group: '%s'", name)
    if get_group_uuid(name):
        LOG.error("Ignoring request, group already exists!")
    token = get_admin_token()
    conn = http.client.HTTPConnection(SDC_SCORE_API_HOST, SDC_SCORE_API_PORT)
    headers = {
        "Authorization": "Bearer " + token["access_token"],
        "Content-Type": "multipart/form-data",
        "Accept": "application/json",
    }
    params = urllib.parse.urlencode({"name": name})
    conn.request("POST", "/groups" + "?" + params, headers=headers)
    resp = conn.getresponse()
    data = json.loads(resp.read().decode("utf-8"))
    conn.close()
    if resp.status == HTTPStatus.OK:
        LOG.info("Sucessfully added group '%s', uuid = %s", name, data)
    else:
        LOG.error("Failed to add group. %s : %s (%s)", resp.status, resp.reason, data)


def group_delete(name: str):
    """Remove a group.

    Args:
        name(str): Group name

    """
    name = " ".join(name)
    uuid = get_group_uuid(name)
    LOG.info("Deleteing group: '%s' (%s)", name, uuid)
    token = get_admin_token()
    conn = http.client.HTTPConnection(SDC_SCORE_API_HOST, SDC_SCORE_API_PORT)
    headers = {
        "Authorization": "Bearer " + token["access_token"],
        "Content-Type": "multipart/form-data",
        "Accept": "application/json",
    }
    params = urllib.parse.urlencode({"groupId": uuid})
    conn.request("DELETE", "/groups" + "?" + params, headers=headers)
    resp = conn.getresponse()
    data = json.loads(resp.read().decode("utf-8"))
    conn.close()
    if resp.status == HTTPStatus.OK:
        LOG.info("Sucessfully deleted group '%s', uuid = %s", name, data)
    else:
        LOG.error(
            "Failed to delete group. '%s' : %s (%s)", resp.status, resp.reason, data
        )

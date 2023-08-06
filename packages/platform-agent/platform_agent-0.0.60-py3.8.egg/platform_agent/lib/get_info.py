import os
import logging
import socket
import requests

import docker
from requests.exceptions import ConnectionError
from urllib3.exceptions import ProtocolError, NewConnectionError

from platform_agent.docker_api.helpers import format_networks_result, format_container_result
from platform_agent.config.settings import Config

logger = logging.getLogger()


def get_ip_addr():
    try:
        resp = requests.get("https://ip.noia.network/")
        return {
            "external_ip": resp.json()
        }
    except NewConnectionError:
        return {}

def get_location():
    return {
        "location_lat": os.environ.get('NOIA_LAT'),
        "location_lon": os.environ.get('NOIA_LON'),
        "location_city": os.environ.get('NOIA_CITY')
    }


def get_network_info():
    network_info = []
    if os.environ.get("NOIA_NETWORK_API", '').lower() == "docker":
        try:
            docker_client = docker.from_env()
            networks = docker_client.networks()
            network_info = format_networks_result(networks)
        except (ProtocolError, ConnectionError):
            network_info = []
    network_info.extend(Config.get_valid_allowed_ips())
    return {
        "network_info": network_info
    }


def get_container_results():
    container_info = []
    if os.environ.get("NOIA_NETWORK_API", '').lower() == "docker":
        try:
            docker_client = docker.from_env()
            networks = docker_client.containers()
            container_info = format_container_result(networks)
        except (ProtocolError, ConnectionError):
            container_info = []
    return {
        "container_info": container_info
    }


def get_info():
    return {
        "agent_name": os.environ.get('NOIA_AGENT_NAME', socket.gethostname()),
        "agent_provider": os.environ.get('NOIA_PROVIDER', None),
        "agent_category": os.environ.get('NOIA_CATEGORY', None),
        "agent_tags": Config.get_list_item('tags'),
        "network_ids": Config.get_list_item('network_ids'),
    }


def gather_initial_info():
    Config()
    result = {}
    result.update(get_ip_addr())
    result.update(get_network_info())
    result.update(get_info())
    result.update(get_container_results())
    return result

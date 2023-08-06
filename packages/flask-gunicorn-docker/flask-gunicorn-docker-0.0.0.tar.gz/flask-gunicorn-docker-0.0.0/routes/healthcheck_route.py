from dataclasses import dataclass
from dataclasses_json import dataclass_json
import requests
from flask import Blueprint

health_check_blueprint = Blueprint(__name__, __name__)


@dataclass_json
@dataclass
class HealthCheckResponse:
    message: str = "OK"


@health_check_blueprint.route('/healthcheck')
@health_check_blueprint.route('/health')
def route():
    try:
        requests.get('http://google.com')
    except:
        raise ValueError("Unhealthy")
    else:
        return HealthCheckResponse().to_json()

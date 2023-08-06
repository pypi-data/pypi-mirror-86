"""An example prediction route where you can plug in the
machine learning model.
"""
from flask import Request, Blueprint
from dataclasses import dataclass
from dataclasses_json import dataclass_json

prediction_blueprint = Blueprint(__name__, __name__)


@dataclass_json
@dataclass
class PredictionResponse:
    score: float = None
    features: list = None
    message: str = "OK"
    latency: float = None


@prediction_blueprint.route("/prediction")
def route():
    try:
        # Calling the model's predict/forward/inference method.
        raise NotImplementedError
    except Exception:
        raise ValueError("Error in prediction")
    else:
        """Using JSON as the default return format.

        Feel free to change to your need.
        """
        return PredictionResponse().to_json()

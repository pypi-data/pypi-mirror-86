from routes.healthcheck_route import health_check_blueprint
from routes.prediction_route import prediction_blueprint

enabled_blueprints = [health_check_blueprint, prediction_blueprint]

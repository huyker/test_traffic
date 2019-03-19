# -*- coding: utf-8 -*-
import re
import json
import traceback
from time import strftime
from flask import Flask, request
from app.api import v1 as api_v1
from app.api import v2 as api_v2
from app.api import v3 as api_v3

from .settings import ProdConfig
from app.extensions import logger, logger_internal_error
from app.utils import send_response
from app.const import CURRENT_VERSION
import flask_monitoringdashboard as dashboard

def create_app(config_object=ProdConfig, content='app'):
    """
    Init App
    :param config_object:
    :param content:
    :return:
    """
    app = Flask(__name__, static_url_path="", static_folder="./template", template_folder="./template")
    dashboard.bind(app)
    app.config.from_object(config_object)
    register_extensions(app, content)
    register_blueprints(app)
    return app


def register_extensions(app, content):
    """
    Init extension
    :param app:
    :param content:
    :return:
    """

    @app.after_request
    def after_request(response):
        # This IF avoids the duplication of registry in the log,
        # since that 500 is already logged via @app.errorhandler.
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s \nREQUEST Body: %s\nRESPONSE: %s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     response.status,
                     json.dumps(request.get_json()),
                     json.dumps(response.get_json())
                     )
        return response

    @app.errorhandler(Exception)
    def exceptions(e):
        print(e)
        return send_response(message="INTERNAL SERVER ERROR", code=500)


def register_blueprints(app):
    """
    Init blueprint for api url
    :param app:
    :return:
    """
    app.register_blueprint(api_v1.orchestrator.api, url_prefix='/api/v1.0')
    app.register_blueprint(api_v2.orchestrator.api, url_prefix='/api/v2.0')
    app.register_blueprint(api_v3.orchestrator.api, url_prefix='/api/v3.0')

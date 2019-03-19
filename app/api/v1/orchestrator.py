from flask import Blueprint
from marshmallow import fields
from app.utils import parse_req, send_response, send_result
from app.handler.v1.orchestrator_handler import detection_handler, get_bounding_box_handler, disconnect_handler, \
    heartbeat_handle

api = Blueprint('v1.0', __name__)


@api.route('/post', methods=['POST'])
def detection():
    return send_result(message="POST Success", code=200, version="v1")


@api.route('/get', methods=['GET'])
def get_bounding_box():
    return send_result(message="GET Success", code=200, version="v1")


@api.route('/delete/<id>', methods=['DELETE'])
def disconnect(id):
    return send_result(message="DELETE Success", code=200, version="v1")


@api.route('/PUT/<id>', methods=['PUT'])
def change_parameters(id):
    return send_result(message="PUT Success", code=200, version="v1")

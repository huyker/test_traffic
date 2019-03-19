from marshmallow import fields, Schema, validate as validate_
from .extensions import parser
from flask import jsonify
from app.const import BOX_PATH


class FieldString(fields.String):
    """
    validate string field, max length = 1024
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 1024  # 1 kB

    def __init__(self, validate=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldString, self).__init__(validate=validate, **metadata)


class FieldNumber(fields.Number):
    """
    validate number field, max length = 30
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 30  # 1 kB

    def __init__(self, validate=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldNumber, self).__init__(validate=validate, **metadata)


def parse_req(argmap):
    """
    Parser request from client
    :param argmap:
    :return:
    """
    return parser.parse(argmap)


def send_response(data=None, message="Error", code=400):
    """"

    """
    res_error = {
        "status_code": code,
        "message": message,
    }
    return jsonify(res_error), code


def send_result(message="Success", code=200, version="v1"):
    """
    Args:
        data: simple result object like dict, string or list
        message: message send to client, default = OK
        code: code default = 200
    Returns:
        json rendered sting result
    """
    res = {
        "status_code": code,
        "message": message,
        "version": version
    }
    return jsonify(res), 200

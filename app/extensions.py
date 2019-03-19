# -*- coding: utf-8 -*-
import configparser
import paho.mqtt.client as paho_client
import uuid
import logging
from webargs.flaskparser import FlaskParser
from logging.handlers import RotatingFileHandler
from app.const import TOPIC_RESPONSE_HEART_BEAT

parser = FlaskParser()
list_detection_id_running = ()
information_threads = []
#logger  Request
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30)
logger = logging.getLogger('api')
logger.setLevel(logging.ERROR)
logger.addHandler(app_log_handler)

#logger internal error
app_log_internal_error_handler = RotatingFileHandler('logs/app_internal_error.log', maxBytes=1000000, backupCount=30)
logger_internal_error = logging.getLogger('internal_error')
logger_internal_error.setLevel(logging.ERROR)
logger_internal_error.addHandler(app_log_internal_error_handler)
# Mosquitto
topic_frame = '/frame'
topic_box = '/json'
frame_pub_client = paho_client.Client(client_id=str(uuid.uuid4()))
frame_pub_client.connect(host='localhost')
frame_pub_client.loop_start()
heart_beat_pub_client = paho_client.Client(client_id=str(uuid.uuid4()))
heart_beat_pub_client.connect(host='localhost')
heart_beat_pub_client.loop_start()
heart_beat_sub_client = paho_client.Client(client_id=str(uuid.uuid4()))
heart_beat_sub_client.connect(host='localhost')
heart_beat_sub_client.subscribe(TOPIC_RESPONSE_HEART_BEAT)
heart_beat_sub_client.loop_start()

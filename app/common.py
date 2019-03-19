import os, json
import configparser
import os
import traceback
from time import strftime
from flask import request
from app.extensions import logger
from app.utils import send_response


def get_host_info():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']['Host'], config['DEFAULT']['Port']


def initialize_paho_client(frame_pub_client):
    frame_pub_client.connect(host='localhost')
    frame_pub_client.loop_start()
    # .on_publish = on_publish_callback


def stop_all_loop(frame_pub_client):
    frame_pub_client.loop_stop()
    frame_pub_client.disconnect()


def get_meta_data_file(frame_path, list_path, box_path, detection_id):
    file_info = {
        "frameTimeStamp": int(os.path.getctime(frame_path)),
        'size': os.path.getsize(frame_path),
        'frame_absolute_path': frame_path,
        'frame_id': os.path.basename(frame_path),
        'list_path': list_path,
        'box_path': box_path,
        'detection_id': detection_id
    }
    return json.dumps(file_info)


def get_stack_frame_id(frame_index, skip=1):
    if (frame_index - 2 * skip) < 0:
        return get_stack_frame_id(frame_index, skip - 1)
    return frame_index - 2 * skip, frame_index - skip, frame_index

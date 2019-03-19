import ast
import cv2
import json
import os
import uuid
import threading
from app.extensions import frame_pub_client, information_threads, logger, heart_beat_sub_client, \
    heart_beat_pub_client
from app.const import SKIP_FRAME, TOPIC_FRAME, FRAME_NAME, MAX_FRAME, FOLDER_STORE_FRAME, RTSP_URL, STATUS_RUNNING, \
    STATUS_STOPPED, BOX_PATH, TOPIC_CHECK_HEART_BEAT, OBJECT_TYPES, CAMERA_TYPE_IR, RTSP_URL_NO_AUTH, MAX_FREQUENCY, \
    BLANK
from app.common import get_meta_data_file, get_stack_frame_id
from app.utils import send_response, send_result
import time
from flask import jsonify

heart_beat = {}


def detection_handler(json_data, detection_id=None):
    # Get data
    try:
        rtsps = json_data.get('rtsps')
        qos = json_data.get('qos')
    except Exception as e:
        return send_response(message='Internal Error Server', code=500)
    # validate rtsp
    try:
        if not rtsps:
            return send_response(message='Cannot found rtsps', code=420)
        for rtsp in rtsps:
            try:
                rtsp_ip = rtsp["rtsp_ip"]
            except Exception as e:
                return send_response(message='Cannot found rtsp server ip and / or port', code=421)
            try:
                rtsp_port = rtsp["rtsp_port"]
            except Exception as e:
                return send_response(message='Cannot found rtsp server ip and / or port', code=421)
            try:
                username = rtsp["username"]
            except Exception as e:
                return send_response(message='Cannot found rtsp username and / or password', code=422)
            try:
                password = rtsp["password"]
            except Exception as e:
                return send_response(message='Cannot found rtsp username and / or password', code=422)
            try:
                url = rtsp["url"]
            except Exception as e:
                return send_response(message='Cannot found rtsp url', code=423)
            try:
                type = rtsp["type"]
            except Exception as e:
                return send_response(message='Cannot found camera type', code=424)

            # check type
            # if not isinstance(rtsp_ip, str) or not isinstance(rtsp_port, int) or not isinstance(url,
            #                                                                                     str) or not isinstance(
            #     username, str) or not isinstance(password, str) or not isinstance(type, str):
            #     return send_response(message='invalid data', code=400)
            if not isinstance(rtsp_ip, str) or BLANK in rtsp_ip:
                return send_response(message='Invalid rtsp server ip and / or port', code=413)
            if not isinstance(rtsp_port, int):
                return send_response(message='Invalid rtsp server ip and / or port', code=413)
            if not isinstance(url, str) or BLANK in url:
                return send_response(message='Invalid rtsp url', code=415)
            if not isinstance(username, str) or BLANK in username:
                return send_response(message='Invalid rtsp username and / or password', code=414)
            if not isinstance(password, str) or BLANK in password:
                return send_response(message='Invalid rtsp username and / or password', code=414)
            if not isinstance(type, str):
                return send_response(message='Invalid camera type', code=416)

            # check len
            if len(rtsp_ip) == 0:
                return send_response(message='Invalid rtsp server ip and / or port', code=413)
            if rtsp_port <= 0 or rtsp_port > 65535:
                return send_response(message='Invalid rtsp server ip and / or port', code=413)
            if len(str(rtsp_port)) == 0:
                return send_response(message='IInvalid rtsp server ip and / or port', code=413)
            if (len(username) != 0 and len(password) == 0) or (len(username) == 0 and len(password) != 0):
                return send_response(message='Both username and password must be filled or empty at the same time',
                                     code=418)
            if len(url) == 0:
                return send_response(message='Invalid rtsp url', code=415)
            if len(type) == 0:
                return send_response(message='Invalid camera type', code=416)
    except Exception as e:
        return send_response(message='Internal Error Server', code=500)

    # Todo: api v1 support only 1 thread
    for tmp_thread in information_threads:
        if tmp_thread["status"] == STATUS_RUNNING:
            if not detection_id:
                return send_response(message='This version is support only 1 camera. Detection_id ' + tmp_thread[
                    "detection_id"] + ' is running.', code=433)
            if tmp_thread["detection_id"] != detection_id:
                return send_response(message="Invalid Detection_id: " + detection_id, code=432)
        else:
            information_threads.remove(tmp_thread)
    rtsp_url = None
    for rtsp in rtsps:
        if rtsp["type"] == CAMERA_TYPE_IR:
            rtsp_ip = rtsp["rtsp_ip"]
            rtsp_port = rtsp["rtsp_port"]
            username = rtsp["username"]
            password = rtsp["password"]
            url = rtsp["url"]
            # validate URL:
            if url[0] != "/":
                url = ''.join(('/', url))
            # rtsp url
            if len(username) > 0:
                rtsp_url = RTSP_URL.format(username, password, rtsp_ip, rtsp_port, url)
                print("Connect to :" + RTSP_URL.format("******", "******", rtsp_ip, rtsp_port, url))
            else:
                rtsp_url = RTSP_URL_NO_AUTH.format(rtsp_ip, rtsp_port, url)
                print("Connect to :" + rtsp_url)

            break
    # Todo: This ver support only IR Camera
    if not rtsp_url:
        return send_response(message="Invalid camera type",
                             code=416)

    # Check rtsp url
    is_success = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG).read()[0]
    if not is_success:
        if len(username) > 0:
            rtsp_url = RTSP_URL.format("******", "******", rtsp_ip, rtsp_port, url)
        return send_response(
            message="Can't connect to this RTSP : " + rtsp_url + ".This RTSP is not exist or invalid protocol.",
            code=425)

    # validate qos
    if qos:
        try:
            timeout = qos['timeout']
        except Exception as e:
            return send_response(message='Cannot found qos:timeout', code=426)
        try:
            frequency = qos['frequency']
        except Exception as e:
            return send_response(message='Cannot found qos:frequency', code=427)

        try:
            object_types = qos['object_types']
        except Exception as e:
            return send_response(message='Cannot found qos:object_types', code=428)

        if len(str(timeout)) == 0:
            return send_response(message='Invalid qos:timeout', code=429)
        if len(str(frequency)) == 0:
            return send_response(message='Invalid qos:frequency', code=430)
        if not object_types:
            return send_response(message='Invalid qos:object_types', code=431)
        if not isinstance(timeout, int):
            return send_response(message='Invalid qos:timeout', code=429)
        if not isinstance(frequency, int):
            return send_response(message='Invalid qos:frequency', code=430)
        if not isinstance(object_types, list):
            return send_response(message='Invalid qos:object_types', code=431)
        if not all(isinstance(item, str) for item in object_types):
            return send_response(message='Invalid qos:object_types', code=431)

        if frequency <= 0:
            return send_response(message='Invalid qos:frequency', code=430)
        if timeout <= 0:
            return send_response(message='Invalid qos:timeout', code=429)

        list_object_not_supported = []
        str_object_not_supported = ""
        for object_type in object_types:
            if object_type not in OBJECT_TYPES:
                list_object_not_supported.append(object_type)
                if object_type not in str_object_not_supported:
                    str_object_not_supported = str_object_not_supported + object_type + ","
        if len(list_object_not_supported) == len(object_types):
            return send_response(message='Requested object_types invalid', code=417)

        if len(str_object_not_supported) > 0:
            return send_response(
                message='qos:object_types: ' + str_object_not_supported[
                                               0:len(str_object_not_supported) - 1] + ' not supported', code=201)
        if OBJECT_TYPES[2] in object_types:
            qos["object_types"] = [OBJECT_TYPES[2]]
        else:
            # remove duplicate value
            qos["object_types"] = list(dict.fromkeys(qos["object_types"]))
        # process frequency
        if frequency > MAX_FREQUENCY:
            return send_response(
                message='qos:frequency recalibrated', code=202)
        qos['timeout'] = qos['timeout'] * 10
    else:
        qos = {
            "timeout": 10,
            "frequency": 2,
            "object_types": ["drones"]
        }
        json_data["qos"] = qos
    # validate detection_id
    if detection_id:
        if len(information_threads) == 0:
            return send_response(message="Invalid Detection_id: " + detection_id, code=432)
        else:
            delete_detection_id(detection_id)
    else:
        detection_id = str(uuid.uuid4())
    # Store json data

    json_thread = {
        "detection_id": detection_id,
        "status": STATUS_RUNNING,
        "last_request_time": time.time(),
        "json_data": json_data
    }
    information_threads.append(json_thread)
    # Create thread for detection
    # rtsp_url = "C:\\Users\\BootAI\\Desktop\\hensolt_13_11\\vlc-record-2018-09-21-13h09m07s-rtsp___192.168.22.60_thermal-.mp4"
    thread = threading.Thread(target=process_data, args=(rtsp_url, detection_id))
    thread.start()
    # Process timeout

    thread_timeout = threading.Thread(target=process_timeout, args=(detection_id,))
    thread_timeout.start()
    return send_result(detection_id, qos=qos)


def process_data(rtsp_url, detection_id):
    for thread in information_threads:
        if detection_id == thread["detection_id"]:
            try:
                video_capture = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            except Exception as e:
                logger.error("Can't connect to " + rtsp_url + "\n" + e)
                thread["status"] == STATUS_STOPPED

            success, image = video_capture.read()
            # check exist folder
            if os.path.exists(FOLDER_STORE_FRAME) is False:
                os.makedirs(FOLDER_STORE_FRAME)
            path_template = FOLDER_STORE_FRAME + FRAME_NAME
            count = 0
            list_frame_paths = []
            while success and thread["status"] == STATUS_RUNNING:
                # extract frame
                frame_path = path_template.format(count)

                cv2.imwrite(frame_path, image)
                list_frame_paths.append(frame_path)
                stack_path = [list_frame_paths[index] for index in
                              list(get_stack_frame_id(len(list_frame_paths) - 1, SKIP_FRAME))]

                # Get data infomation
                file_infomation = get_meta_data_file(frame_path, stack_path, BOX_PATH, detection_id)

                # Publish file_infomation
                frame_pub_client.publish(TOPIC_FRAME, file_infomation)

                # Pop first element
                if len(list_frame_paths) > MAX_FRAME:
                    try:
                        os.remove(list_frame_paths.pop(0))
                    except Exception as e:
                        pass
                        # logger.error('Error Remove Frame: ' + list_frame_paths[0])
                count += 1
                try:
                    success, image = video_capture.read()
                except Exception as e:
                    logger.error("Error read frame")
                    logger.error(e)
                    break
            thread["status"] = STATUS_STOPPED


def process_timeout(detection_id):
    for thread in information_threads:
        if detection_id == thread["detection_id"]:
            time_out = thread["json_data"]["qos"]["timeout"]
            while thread['status'] == STATUS_RUNNING:
                if (time.time() - thread["last_request_time"] > time_out):
                    # thread['status'] = STATUS_STOPPED
                    delete_detection_id(detection_id)
                    break
                time.sleep(1)


def get_bounding_box_handler(detection_id):
    for thread in information_threads:
        if thread["detection_id"] == detection_id and thread["status"] == STATUS_RUNNING:
            # Refresh last time request of thread
            thread["last_request_time"] = time.time()
            # Get data
            response = open(BOX_PATH, "r").read()
            response = json.loads(response)
            if 'qos' in thread["json_data"].keys():
                object_types = thread["json_data"]["qos"]["object_types"]
                if OBJECT_TYPES[2] not in thread["json_data"]["qos"]["object_types"]:
                    for item in response["detection_objects"]:
                        if item["object_type"] not in object_types:
                            response["detection_objects"].remove(item)
            return jsonify(response)
    return send_response(message="Invalid Detection_id: " + detection_id, code=432)


def disconnect_handler(detection_id):
    if delete_detection_id(detection_id):
        return send_response(message="Success", code=200)
    return send_response(message="Invalid Detection_id: " + detection_id, code=432)


def heartbeat_handle():
    global heart_beat
    heart_beat_id = str(uuid.uuid4())
    heart_beat = {
        "heart_beat_id": heart_beat_id,
        "status": "checking"
    }
    heart_beat_pub_client.publish(TOPIC_CHECK_HEART_BEAT, json.dumps(heart_beat))
    time.sleep(0.1)
    if heart_beat["heart_beat_id"] == heart_beat_id and heart_beat["status"] == "OK":
        return send_response(message="Success", code=200)
    return send_response(message='Backend System Unreachable – Out of Service', code=501)


def delete_detection_id(detection_id):
    for thread in information_threads:
        if thread['detection_id'] == detection_id:
            thread['status'] = STATUS_STOPPED
            information_threads.remove(thread)
            return True
    return False


def on_message_check_heart_beat(client, userdata, msg):
    global heart_beat
    heart_beat = ast.literal_eval(msg.payload.decode("utf-8"))


heart_beat_sub_client.on_message = on_message_check_heart_beat

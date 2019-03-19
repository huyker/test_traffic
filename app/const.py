from pathlib import Path

MYPATH = Path().absolute()

SKIP_FRAME = 2
TOPIC_FRAME = "/frame"
FRAME_NAME = "/frame{}.JPG"
TOPIC_CHECK_HEART_BEAT = '/check_heart_beat'
TOPIC_RESPONSE_HEART_BEAT = '/response_heart_beat'
MAX_FRAME = 500
FOLDER_STORE_FRAME = str(MYPATH) + "/outputs/cameraname"
HEART_BEAT_FRAME = str(MYPATH) + "/app/heartbeat/frame_test.JPG"
RTSP_URL = "rtsp://{}:{}@{}:{}{}"
RTSP_URL_NO_AUTH = "rtsp://{}:{}{}"
STATUS_RUNNING = "RUNNING"
STATUS_STOPPED = "STOPPED"
BOX_PATH = str(MYPATH) + "/response/box.txt"
HEART_BEAT_PATH = str(MYPATH) + "/response/heart_beat.txt"
OBJECT_TYPES = ["drones", "birds", "all"]
CAMERA_TYPE_IR = "IR"
CURRENT_VERSION = "V1.00"
MAX_FREQUENCY = 5
BLANK = " "

from app.app import create_app
from app.settings import DevConfig, ProdConfig, os
from app.common import get_host_info
CONFIG = ProdConfig

app = create_app(config_object=CONFIG)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True, use_reloader=True, debug=False)

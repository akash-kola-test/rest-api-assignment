import pathlib
import logging
import logging.config as logging_config
import json
import atexit
from app import app


def setup_logger():
    config_file = pathlib.Path("src/config/log_config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging_config.dictConfig(config)
    # queue_handler = logging.getHandlerByName("queue_handler")
    # if queue_handler is not None:
    #     queue_handler.listener.start()
    #     atexit.register(queue_handler.listener.stop)



if __name__ == "__main__":
    setup_logger()
    app.run(debug=True)

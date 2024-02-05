import logging.config
import os
import json

log_config_path = os.path.join(os.path.dirname(__file__), 'log_config.json')

with open(log_config_path, 'rt') as f:
    config = json.load(f)

logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

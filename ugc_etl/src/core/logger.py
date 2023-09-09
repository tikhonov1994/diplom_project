import logging
import sys

from src.core.config import app_config

logging.basicConfig(filename=app_config.log_filename, level=app_config.logging_level,
                    format='%(asctime)s  %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logger = logging.getLogger(__name__)
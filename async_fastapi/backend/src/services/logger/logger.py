import os
import pathlib

from loguru import logger

srcpath = pathlib.Path(__file__).parent.parent.parent
logs_full_path = os.path.join(srcpath, 'CryptoTrader_logs.log')

logger.remove()
logger.add(logs_full_path,
           level='DEBUG',
           rotation='100 MB',
           compression='zip',
           format='{time: DD.MM.YYYY HH:mm:ss} - {module} - {level} - {message}'
           )

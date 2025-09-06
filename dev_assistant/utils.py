import logging

logger = logging.getLogger('dev_assistant')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler('dev_assistant.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

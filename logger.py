import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     filename="log_file.log",
#     format="%(asctime)s %(levelname)s %(module)s => %(message)s",
#     datefmt="%d-%m-%Y %H:%M:%S",
# )

# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

class Logger:
    def logger_func(file_name='log_file.log', log_level=logging.DEBUG):
        logger = logging.getLogger('demo')
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('log_file.log')
        formater = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        console_handler.setFormatter(formater)
        file_handler.setFormatter(formater)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        return logger

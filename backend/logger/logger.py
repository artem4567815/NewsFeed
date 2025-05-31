import logging

class Logger:
    def __init__(self, log_level=logging.DEBUG):
        self.logger = logging.getLogger("AdvancedLogger")
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            log_format = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_format)
            self.logger.addHandler(console_handler)


    def log(self, level: str, message: str):
        level = level.lower()
        if level == "debug":
            self.logger.debug(message)
        elif level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "critical":
            self.logger.critical(message)
        else:
            self.logger.error(f"Некорректный уровень логирования: {level}")

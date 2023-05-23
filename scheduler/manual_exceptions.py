from logger import logger


class JobExecutionException(Exception):
    def __init__(self, message):
        self.exception_message = message
        self._record_logs()

    def __str__(self):
        if self.exception_message:
            return f'Job execution failed with reason: {self.exception_message}'
        else:
            return 'Job execution failed with unknown reason'

    def _record_logs(self):
        logger.error(f'Job execution failed with reason: {self.exception_message}')

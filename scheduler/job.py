from dataclasses import dataclass, field
from datetime import datetime, date
from typing import NamedTuple
import threading
import os
import sys

from tasks import Tasks
from manual_exceptions import JobExecutionException
from logger import logger

inter_version = sys.version.split(' ')[0]


class Parameters(NamedTuple):
    direction: str
    filename: str
    text: str
    url: str


@dataclass
class Job:
    file_name: str = field(default='')
    id: int = field(default=-1)
    job_type: str = field(default='')
    name: str = field(default='')
    parameters: dict = field(default_factory=dict)
    start_at: str = field(default='')
    max_working_time: int = field(default=-1)
    tries: int = field(default=-1)
    repeat: bool = field(default=False)
    dependencies: list['Job'] = field(default_factory=list)

    def run(self) -> None:
        logger.info(f'This is job: {self.file_name}')
        logger.info(f'This job type: {self.job_type}')
        logger.info(f'This Thread PID: {threading.current_thread().ident}')
        parameters_value = self._to_distribute_values()
        if self.start_at == '':
            if inter_version.split('.')[1] == 9:
                self._start_job_elif(parameters_value)
            else:
                self._start_job(self.job_type, parameters_value)
        else:
            start_time = self._get_start_time().strftime('%Y-%m-%d %H:%M')
            while True:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                if start_time == current_time:
                    if inter_version.split('.')[1] == 9:
                        self._start_job_elif(parameters_value)
                    else:
                        self._start_job(self.job_type, parameters_value)
                    break
                elif start_time < current_time:
                    break

    def _to_distribute_values(self):
        parameters_value = Parameters(
            direction=self.parameters['direction'],
            filename=self.parameters['filename'],
            text=self.parameters['text'],
            url=self.parameters['URL']
        )
        return parameters_value

    def _start_job_elif(self, props) -> None:
        try:
            if self.job_type == 'create_dir':
                Tasks.create_dir(props.direction)
            elif self.job_type == 'delete_dir':
                Tasks.create_dir(props.direction)
            elif self.job_type == 'create_file':
                Tasks.create_file(props.direction, props.filename)
            elif self.job_type == 'delete_file':
                Tasks.delete_file(props.direction, props.filename)
            elif self.job_type == 'write_file':
                Tasks.write_file(props.direction, props.filename, props.text)
            elif self.job_type == 'read_file':
                Tasks.read_file(props.direction, props.filename)
            elif self.job_type == 'get_request':
                Tasks.get_request(props.url)
            elif self.job_type == 'analyze_response':
                Tasks.analyze_response()
        except JobExecutionException:
            self._update_status_for_job('failed')
        else:
            logger.info(f'We done with Job: {self.file_name}')
            self._update_status_for_job('success')

    def _start_job(self, j_type: str, props: Parameters) -> None:
        try:
            match j_type:
                case 'create_dir':
                    Tasks.create_dir(props.direction)
                case 'delete_dir':
                    Tasks.delete_dir(props.direction)
                case 'create_file':
                    Tasks.create_file(props.direction, props.filename)
                case 'delete_file':
                    Tasks.delete_file(props.direction, props.filename)
                case 'write_file':
                    Tasks.write_file(props.direction, props.filename, props.text)
                case 'read_file':
                    Tasks.read_file(props.direction, props.filename)
                case 'get_request':
                    Tasks.get_request(props.url)
                case 'analyze_response':
                    Tasks.analyze_response()
        except JobExecutionException:
            self._update_status_for_job('failed')
        else:
            logger.info(f'We done with Job: {self.file_name}')
            self._update_status_for_job('success')

    @staticmethod
    def _get_current_statuses():
        current_status = []
        while True:
            try:
                os.rename('scheduler_status.csv', 'scheduler_status.csv')
                with open('scheduler_status.csv', 'r') as file:
                    for line in file.readlines():
                        if line.replace('\n', ''):
                            current_status.append(line.replace('\n', ''))
                break
            except OSError:
                logger.DEBUG(f'file is busy')
                continue
        return current_status

    def _update_status_for_job(self, status: str) -> None:
        current_status = self._get_current_statuses()
        job_with_new_status_text = ''
        for jobs in current_status:
            if self.file_name in jobs:
                new_status_for_job = jobs.split(';')
                new_status_for_job[3] = status
                job_with_new_status_text = ';'.join(
                    str(new_status_for_job[k]) for k in range(0, len(new_status_for_job)))
                current_status.remove(jobs)
                break

        if job_with_new_status_text:
            current_status.append(job_with_new_status_text)
            self._save_new_statuses(current_status)

    @staticmethod
    def _save_new_statuses(new_status) -> None:
        while True:
            try:
                os.rename('scheduler_status.csv', 'scheduler_status.csv')
                with open('scheduler_status.csv', 'w') as file:
                    for line in new_status:
                        file.write(line + '\n')
                break
            except OSError:
                logger.DEBUG(f'file is busy')
                continue

    def _get_start_time(self) -> datetime:
        return datetime.strptime(f'{date.today()} {self.start_at}', '%Y-%m-%d %H:%M')

    def pause(self):
        pass

    def stop(self):
        pass

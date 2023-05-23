from dataclasses import dataclass, field
from typing import Generator
from threading import Thread
import pickle
import os

from logger import logger
from job import Job


@dataclass
class Scheduler:
    pool_size: int = field(default=3)
    current_jobs: list = field(default_factory=list)
    status_dict: dict = field(default_factory=dict)
    status_list: list = field(default_factory=list)
    jobs_dict_for_run: dict = field(default_factory=dict)
    list_of_threaded_jobs: list = field(default_factory=list)
    jobs_attempts_counter: dict = field(default_factory=dict)
    job_dict_with_status: dict = field(default_factory=dict)
    file_with_jobs_status: str = field(default='scheduler_status.csv')

    def schedule(self) -> Generator:
        while True:
            yield
            self._get_list_of_tasks_from_file()
            self._get_list_of_jobs_for_run()
            self._run_jobs()

    def resume_jobs(self) -> Generator:
        while True:
            yield
            self._update_list_of_jobs_for_run()
            self._run_jobs()

    def run(self) -> Generator:
        while True:
            yield

    def restart(self) -> Generator:
        while True:
            yield

    def stop(self) -> Generator:
        while True:
            yield

    def _run_job_on_new_thread(self) -> Generator:
        while True:
            job, name = (yield)
            self._remove_job_from_list_if_success()
            if name not in self.list_of_threaded_jobs:
                thread_job = Thread(target=job.run, name=name, daemon=True)
                if len(self.list_of_threaded_jobs) < self.pool_size:
                    self._count_job_attempts(name)
                    if int(self.jobs_attempts_counter[name]) <= job.tries or job.tries == -1:
                        self.list_of_threaded_jobs.append(thread_job.name)
                        logger.info(f'We run new job in new thread. Job name: {thread_job.name}')
                        thread_job.start()
                    elif int(self.jobs_attempts_counter[name]) > job.tries:
                        self._put_stopped_status_to_job(name)

    def _remove_job_from_list_if_success(self) -> None:
        self._update_status_dict()
        for job in self.list_of_threaded_jobs:
            if self.status_dict.get(job, None) is not None:
                if self.status_dict.get(job, None) in ['success', 'failed', 'stopped']:
                    self.list_of_threaded_jobs.remove(job)

    def _update_status_dict(self) -> None:
        self.status_dict = {}
        for row in self.status_list:
            row_data = row.split(';')
            self.status_dict[row_data[2]] = row_data[3]

    def _update_status_list(self) -> None:
        self.status_list = []
        while True:
            try:
                os.rename(self.file_with_jobs_status, self.file_with_jobs_status)
                with open(self.file_with_jobs_status, 'r') as file:
                    for row in file.readlines():
                        if row.replace('\n', ''):
                            self.status_list.append(row.replace('\n', ''))
                break
            except OSError:
                logger.DEBUG(f'file is busy')
                continue

    def _put_stopped_status_to_job(self, job_name: str) -> None:
        job_with_new_status_text = ''
        for jobs in self.status_list:
            if job_name in jobs:
                new_status_for_job = jobs.split(';')
                new_status_for_job[3] = 'stopped'
                job_with_new_status_text = ';'.join(
                    str(new_status_for_job[k]) for k in range(0, len(new_status_for_job)))
                self.status_list.remove(jobs)
                break
        if job_with_new_status_text:
            self.status_list.append(job_with_new_status_text)
            self._save_new_status_to_file()

    def _save_new_status_to_file(self) -> None:
        while True:
            try:
                os.rename(self.file_with_jobs_status, self.file_with_jobs_status)
                with open(self.file_with_jobs_status, 'w') as file:
                    for line in self.status_list:
                        file.write(line + '\n')
                break
            except OSError:
                logger.DEBUG(f'file is busy')
                continue

    def _count_job_attempts(self, name: str) -> None:
        if self.jobs_attempts_counter.get(name) is not None:
            self.jobs_attempts_counter[name] += 1
        else:
            self.jobs_attempts_counter[name] = 1

    def _run_jobs(self) -> None:
        threaded_job = self._run_job_on_new_thread()
        threaded_job.send(None)
        if self.jobs_dict_for_run:
            list_jobs_with_dependencies = []
            while True:
                try:
                    name, job = self.jobs_dict_for_run.popitem()
                    if len(job.dependencies) > 0:
                        if self._check_job_dependencies(job):
                            list_jobs_with_dependencies.append((name, job))
                        else:
                            threaded_job.send((job, name))
                    else:
                        threaded_job.send((job, name))
                    if len(self.jobs_dict_for_run) == 0 and len(list_jobs_with_dependencies) > 0:
                        for dep in list_jobs_with_dependencies:
                            self.jobs_dict_for_run[dep[0]] = dep[1]
                        list_jobs_with_dependencies = []
                except IndexError:
                    break
                except KeyError:
                    break

    def _get_list_of_tasks_from_file(self) -> None:
        self.job_dict_with_status = {}
        self._update_status_list()
        for row in self.status_list:
            row_data = row.split(';')
            self.job_dict_with_status[row_data[2]] = row_data[3]
        self.current_jobs = [key for key, val in self.job_dict_with_status.items() if val != 'success']

    def _get_list_of_jobs_for_run(self) -> None:
        for job_file in self.current_jobs:
            with open(f'jobs/{job_file}.pkl', 'rb') as file:
                job_task = pickle.load(file)
            self.jobs_dict_for_run[job_file] = job_task

    def _update_list_of_jobs_for_run(self) -> None:
        self.current_jobs = []
        self._update_status_list()
        for row in self.status_list:
            row_data = row.split(';')
            if self.job_dict_with_status.get(row_data[2], None) is not None:
                self.job_dict_with_status[row_data[2]] = row_data[3]
        self.current_jobs = [key for key, val in self.job_dict_with_status.items()
                             if val not in ['success', 'stopped']]
        if self.current_jobs:
            self._get_list_of_jobs_for_run()

    def _check_job_dependencies(self, job: Job) -> bool:
        for dep in job.dependencies:
            if dep in self.jobs_dict_for_run:
                return True
        return False

from typing import NamedTuple
import json
import time
import pickle
import uuid
import os
import threading

from scheduler import Scheduler
from job import Job
from logger import logger

job_types = ['create_dir', 'delete_dir', 'create_file', 'delete_file', 'write_file',
             'read_file', 'get_request', 'analyze_response']

scheduler_types = ['restart', 'start', 'stop']

jobs_id_name = {}


class CommandProps(NamedTuple):
    file_name: str
    id: int
    type: str
    name: str
    parameters: dict
    start_at: str
    max_working_time: int
    tries: int
    repeat: bool
    dependencies: list


def event_loop():
    logger.info('Start scheduler')
    logger.info(f'Main Thread PID: {threading.current_thread().ident}')
    if not os.path.isfile('scheduler_status.csv'):
        open('scheduler_status.csv', 'w').close()
    if not os.path.isfile('jobs.json'):
        open('jobs.json', 'w').close()
    scheduler = Scheduler()
    schedule_manager = scheduler.schedule()
    schedule_manager.send(None)
    scheduler_next_job = scheduler.resume_jobs()
    scheduler_next_job.send(None)
    next(schedule_manager)

    while True:
        job_command = False
        scheduler_command = False
        while True:
            time.sleep(1)
            command = _get_command_from_jobs_file()
            if command:
                if command.type in job_types:
                    task = _create_task(command)
                    filename = _save_task_as_file(task)
                    _save_task_status(task.name, filename, 'created')
                    job_command = True
                    break
                if command.type in scheduler_types:
                    scheduler_command = True
                    break
            else:
                next(scheduler_next_job)
        if job_command:
            try:
                logger.info('We got new job and we start it')
                next(schedule_manager)
            except StopIteration:
                continue
        if scheduler_command:
            if command.type == 'restart':
                logger.info('We restart the scheduler')
                schedule_manager.close()
                schedule_manager = scheduler.schedule()
                schedule_manager.send(None)
                logger.info('Scheduler started again...')
                next(schedule_manager)
            elif command.type == 'stop':
                logger.info('We stopped the scheduler')
                schedule_manager.close()
            elif command.type == 'start':
                logger.info('Scheduler started again...')
                schedule_manager = scheduler.schedule()
                schedule_manager.send(None)
                next(schedule_manager)


def _command_parser(job_id: int, command_data: dict) -> CommandProps:
    command_props = CommandProps(
        '',
        job_id,
        command_data['type'],
        command_data['name'],
        command_data['parameters'],
        command_data['start_at'],
        command_data['max_working_time'],
        command_data['tries'],
        command_data['repeat'],
        command_data['dependencies']
    )
    return command_props


def _get_command_from_jobs_file():
    command = ''
    command_dict = {}
    with open('jobs.json', 'r+') as jobs_file:
        try:
            command_dict = json.load(jobs_file)
        except FileNotFoundError:
            logger.WARNING('No file with jobs')
        except json.decoder.JSONDecodeError as e:
            logger.error(f'Bad Job Description: {e}')
        else:
            for key in command_dict:
                command = _command_parser(key, command_dict.pop(key))
                break
        finally:
            jobs_file.seek(0)
            json.dump(command_dict, jobs_file)
            jobs_file.truncate()
    return command


def _create_task(props: CommandProps) -> Job:
    task = Job(
        '',
        props.id,
        props.type,
        props.name,
        props.parameters,
        props.start_at,
        props.max_working_time,
        props.tries,
        props.repeat,
        props.dependencies
    )
    return task


def _save_task_as_file(task: Job) -> str:
    filename = uuid.uuid4().__str__()
    task.file_name = filename
    jobs_id_name[task.id] = filename
    if len(task.dependencies) > 0:
        task.dependencies = _new_dependencies(task.dependencies)
    with open(f'jobs/{filename}.pkl', 'wb') as file:
        pickle.dump(task, file)
    return filename


def _new_dependencies(deps: list) -> list:
    new_deps = []
    for dep in deps:
        if jobs_id_name.get(str(dep), None) is not None:
            new_deps.append(jobs_id_name[str(dep)])
        else:
            new_deps.append(dep)
    return new_deps


def _save_task_status(task_name: str, filename: str, status: str) -> None:
    task_status = f'{int(time.time())};{task_name};{filename};{status}\n'
    with open('scheduler_status.csv', 'a') as file:
        file.write(task_status)


if __name__ == '__main__':
    event_loop()

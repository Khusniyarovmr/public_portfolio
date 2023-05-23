import os

from scheduler import Scheduler
from python_tests.src.scheduler_test_data import (
    JOB_NAMES,
    CHECK_STATUS_DICT,
    CHECK_LIST_OF_TASKS_FROM_FILE,
    first_job_example,
    second_job_example
)

sched = Scheduler()
sched.file_with_jobs_status = './python_tests/src/scheduler_status.csv'


def test_check_job_dependencies():
    sched.jobs_dict_for_run[JOB_NAMES[0]] = first_job_example
    sched.jobs_dict_for_run[JOB_NAMES[1]] = second_job_example
    result_1 = sched._check_job_dependencies(first_job_example)
    result_2 = sched._check_job_dependencies(second_job_example)
    assert result_1 is False
    assert result_2 is True


def test_remove_job_from_list_if_success():
    print(os.getcwd())
    for job_name in JOB_NAMES:
        sched.list_of_threaded_jobs.append(job_name)
    assert len(sched.list_of_threaded_jobs) == 3
    sched._update_status_list()
    sched._remove_job_from_list_if_success()
    assert len(sched.list_of_threaded_jobs) == 2


def test_update_status_dict():
    sched._update_status_list()
    sched._update_status_dict()
    assert sched.status_dict == CHECK_STATUS_DICT


def test_get_list_of_tasks_from_file():
    sched._update_status_list()
    sched._get_list_of_tasks_from_file()
    assert sched.current_jobs == CHECK_LIST_OF_TASKS_FROM_FILE

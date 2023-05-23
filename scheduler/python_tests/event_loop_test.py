# тестировть будем все функции основные
# интерфейсы
import json
from python_tests.src.event_loop_test_data import JOB_DICT
from python_tests.src.data_model_for_job import JobInfoModel
from event_loop import _command_parser, CommandProps
from job import Job


def test_how_load_jobs_from_file():
    with open('./python_tests/src/job_test_data.json', 'r') as f:
        data_from_json = json.load(f)
    assert data_from_json == JOB_DICT
    assert JobInfoModel.parse_obj(data_from_json['0'])


def test_check_command_parser():
    with open('./python_tests/src/job_test_data.json', 'r') as f:
        data_from_json = json.load(f)
    for key, value in data_from_json.items():
        k_data = key
        v_data = value
        break
    # noinspection PyUnboundLocalVariable
    result = _command_parser(k_data, v_data)
    assert type(result) == CommandProps


def test_create_job_func():
    with open('./python_tests/src/job_test_data.json', 'r') as f:
        data_from_json = json.load(f)
    for key, value in data_from_json.items():
        k_data = key
        v_data = value
        break
    # noinspection PyUnboundLocalVariable
    props = JobInfoModel.parse_obj(v_data)
    # noinspection PyUnboundLocalVariable
    result = Job(
        '',
        k_data,
        props.type,
        props.name,
        props.parameters,
        props.start_at,
        props.max_working_time,
        props.tries,
        props.repeat,
        props.dependencies
    )
    assert type(result) == Job

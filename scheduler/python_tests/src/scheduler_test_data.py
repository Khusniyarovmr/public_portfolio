from job import Job
from python_tests.src.data_model_for_job import JobInfoModel

JOBS_DICT = {'0': {'type': 'create_dir', 'name': 'create data dir', 'parameters': {'direction': 'data', 'filename': '', 'text': '', 'URL': ''}, 'start_at': '', 'max_working_time': -1, 'tries': 3, 'repeat': False, 'dependencies': []},
             '1': {'type': 'delete_dir', 'name': 'delete folder data', 'parameters': {'direction': 'data', 'filename': '', 'text': '', 'URL': ''}, 'start_at': '', 'max_working_time': -1, 'tries': 3, 'repeat': False, 'dependencies': ['a221acc3-7a92-4b5e-946c-870fa3940355']}
             }

JOB_NAMES = ['a221acc3-7a92-4b5e-946c-870fa3940355', '53b49193-34bb-41f3-be59-c2d2acaa498b', '96jh9193-65kj-65i7-kl65-c2d2hgit968t']

CHECK_STATUS_DICT = {'a221acc3-7a92-4b5e-946c-870fa3940355': 'created', '53b49193-34bb-41f3-be59-c2d2acaa498b': 'created', '96jh9193-65kj-65i7-kl65-c2d2hgit968t': 'success'}
CHECK_LIST_OF_TASKS_FROM_FILE = ['a221acc3-7a92-4b5e-946c-870fa3940355', '53b49193-34bb-41f3-be59-c2d2acaa498b']

first_job = JobInfoModel.parse_obj(JOBS_DICT['0'])
second_job = JobInfoModel.parse_obj(JOBS_DICT['1'])

first_job_example = Job(
    JOB_NAMES[0],
    0,
    first_job.type,
    first_job.name,
    first_job.parameters,
    first_job.start_at,
    first_job.max_working_time,
    first_job.tries,
    first_job.repeat,
    first_job.dependencies
)

second_job_example = Job(
    JOB_NAMES[1],
    1,
    second_job.type,
    second_job.name,
    second_job.parameters,
    second_job.start_at,
    second_job.max_working_time,
    second_job.tries,
    second_job.repeat,
    second_job.dependencies
)
from pydantic import BaseModel


class Parameters(BaseModel):
    direction: str = ''
    filename: str = ''
    text: str = ''
    URL: str = ''


class JobInfoModel(BaseModel):
    type: str
    name: str = ''
    parameters: Parameters
    start_at: str = ''
    max_working_time: int = -1
    tries: int = -1
    repeat: bool = False
    dependencies: list = []

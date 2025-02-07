import re
import asyncio
from datetime import datetime

from aiofile import async_open
from sqlalchemy.exc import IntegrityError

from src.core.app_settings import app_settings
from src.crud.log import log_crud
from src.crud.message import message_crud
from src.schemes.log import LogCreate
from src.schemes.message import MessageCreate


async def init_log_data():
    filepath = app_settings.BASE_DIR + "/tmp_file/out"
    tasks = []
    async with async_open(filepath, 'r') as f:
        async for row in f:
            row_data = row_parser(row)
            tasks.append(data_processing(row_data=row_data))
    await asyncio.gather(*tasks)
    print('Init log data complete')


def get_id(str_row: str):
    id_match = re.search(r'id=([^\s]+)', str_row)
    if id_match:
        id_value = id_match.group(1)
        return id_value
    else:
        return None


def row_parser(row: str) -> list:
    return row.replace('\n', '').split(' ', 5)


async def data_processing(row_data: list) -> None:
    created = datetime.strptime(row_data[0] + " " + row_data[1], '%Y-%m-%d %H:%M:%S')
    int_id = row_data[2]
    str_row = ' '.join(row_data[2:])

    if len(row_data) == 6 and row_data[3] == '<=':
        id_data = get_id(row_data[5])
        if id_data is None:
            return None
        result = MessageCreate(
            id=id_data,
            created=created,
            int_id=int_id,
            str_row=str_row,
            status=True
        )
        try:
            await message_crud.create(obj_in=result)
        except IntegrityError:
            print(result)
        except Exception as e:
            print(e)
    else:
        result = LogCreate(
            created=created,
            int_id=int_id,
            str_row=str_row,
            address=row_data[4] if len(row_data) >= 5 and row_data[3] in ['<=', '=>', '->', '**', '=='] else None
        )
        try:
            await log_crud.create(obj_in=result)
        except IntegrityError:
            print(result)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(init_log_data())

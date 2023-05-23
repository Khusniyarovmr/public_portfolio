import asyncio
from asyncio.streams import StreamReader, StreamWriter
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from server import Private
from server import Server

loop = asyncio.new_event_loop()
server = Server(host='localhost', port=8000, loop=loop)
writer = StreamWriter
reader = StreamReader


@patch.object(Server, '_read_data_from_socket', return_value=b'John: connected')
@pytest.mark.asyncio
async def test_get_client_name(mocked_function: AsyncMock) -> None:
    result = await server._get_client_name(reader)
    assert result == 'John'


sendfile_mes1 = '/sendfile John /home/marat/async-python-sprint-3/server_local_files/John/testfile.csv;8388608'
sendfile_mes2 = '/sendfile John /home/marat/async-python-sprint-3/server_local_files/John/filefile.csv;1048576'
sendfile_mes3 = '/sendfile Tom /home/marat/async-python-sprint-3/server_local_files/John/testfile.csv;1048576'
getfile_mes = '/getfiles testfile.csv'
file_path = '/home/marat/async-python-sprint-3/server_local_files/John/testfile.csv'


@patch.object(Server, '_write_data_to_socket', return_value=getfile_mes)
@patch.object(Server, '_read_data_from_socket', return_value=file_path)
@pytest.mark.asyncio
async def test_get_file_from_client(mocked_function: AsyncMock, mocked_function_2: AsyncMock) -> None:
    result1 = await server._get_file_from_client(reader, writer, sendfile_mes1)
    assert result1 == False
    result2 = await server._get_file_from_client(reader, writer, sendfile_mes2)
    assert result2 == False
    result3 = await server._get_file_from_client(reader, writer, sendfile_mes3)
    assert result3 == False


def test_server_know_file_receiver() -> None:
    result1 = server._server_know_file_receiver('Tom')
    assert result1 == False
    server.user_names['John'] = 'any'
    result2 = server._server_know_file_receiver('John')
    assert result2 == True


def test_message_counter_manager() -> None:
    result1 = server._message_counter_manager('John')
    assert result1 == True


def test_check_the_client_for_a_ban() -> None:
    current_time_2 = datetime.now().timestamp()
    server.ban_list['John'] = current_time_2 + 1000
    result1 = server._check_the_client_for_a_ban('John')
    assert result1 == True
    result2 = server._check_the_client_for_a_ban('Jane')
    assert result2 == False


data_for_test = '@John yoyoyo yoyo'
result = Private(name='John', data='yoyoyo yoyo')


def test_get_private_name_and_mes() -> None:
    result1 = server._get_private_name_and_mes(data_for_test)
    assert result1 == result

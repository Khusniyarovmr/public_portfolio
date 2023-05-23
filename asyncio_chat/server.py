import asyncio
import os
from asyncio.streams import StreamReader, StreamWriter
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, NamedTuple

import aiofiles

from db_manager import (
    insert_message_into_db,
    get_old_messages_when_online
)
from logger import logger

root = os.path.dirname(__file__)


class Private(NamedTuple):
    name: str
    data: str


@dataclass
class Server:
    connection_counter: ClassVar[int] = field(default=0)
    user_names: ClassVar[dict] = {}
    clients: ClassVar[list] = []
    limit_of_old_messages: ClassVar[int] = field(default=20)
    timeout_for_del_old_messages: ClassVar[int] = field(default=3600)
    ban_counter: ClassVar[dict] = {}
    ban_list: ClassVar[dict] = {}
    ban_timeout: ClassVar[int] = field(default=300)
    message_counter: ClassVar[dict] = {}
    timeout_for_limit_messages: ClassVar[int] = field(default=3600)
    first_message_client_time: ClassVar[dict] = {}
    max_message_counter_per_client: ClassVar[int] = field(default=20)
    limit_size_on_send_file: ClassVar[int] = field(default=5242880)
    host: str = field(default='localhost')
    port: int = field(default=8000)
    loop: asyncio.AbstractEventLoop = ''

    async def _client_connected(self, reader: StreamReader, writer: StreamWriter) -> None:
        self.connection_counter += 1
        name = await self._get_client_name(reader)
        logger.info(f'{name} connected')
        self._create_client_folder_if_not_exists(name)
        self._put_writer_into_clients(writer)
        await self._notify_everyone(name)
        self._put_user_into_user_names(writer, name)
        old_messages = await get_old_messages_when_online(name=name,
                                                          limit=self.limit_of_old_messages,
                                                          timeout=self.timeout_for_del_old_messages)
        await self._put_old_messages_to_writer(writer, old_messages, name)

        while True:
            data = await self._read_data_from_socket(reader)
            message = data.decode().strip()
            if message.startswith('/exit'):
                exit_message = f'{name!r} get out of the chat'
                logger.info(exit_message)
                await self._send_message_to_other_clients(writer, exit_message, name)
                break
            elif message.startswith('/status'):
                await self._get_user_statuses(name)
            elif not self._check_the_client_for_a_ban(name):
                if message.startswith('/ban'):
                    await self._ban_manager(message)
                elif message.startswith('/sendfile'):
                    if await self._get_file_from_client(reader, writer, message):
                        await self._notify_file_receiver(message, name)
                elif message.startswith('/getfiles'):
                    await self._send_ready_for_send_files_to_client(reader, writer, message, name)
                elif message.startswith('@'):
                    private_name, private_message = self._get_private_name_and_mes(message)
                    await self._send_message_in_private_chats(name, private_name, private_message, message, writer)
                    await insert_message_into_db(name, private_name, private_message)
                elif message:
                    if not len(self.clients) == 1:
                        if self._message_counter_manager(name):
                            await self._send_message_to_other_clients(writer, message, name)
                            await insert_message_into_db(name, 'ALL', message)
                        else:
                            await self._send_spam_warning_to_client(name)

        self.clients.remove(writer)
        self.connection_counter -= 1
        writer.close()

    async def _notify_file_receiver(self, message: str, client_name: str) -> None:
        mes_details = message.split()
        to_name = mes_details[1]
        message_to_send = f'{client_name!r} send file for you. Please type "/getfiles" to download'
        if self.user_names.get(to_name, ):
            for writer in self.user_names[to_name]:
                await self._write_data_to_socket(writer, message_to_send)

    async def _send_ready_for_send_files_to_client(self, reader: StreamReader, writer: StreamWriter,
                                                   message: str, client_name: str) -> None:
        filepath = os.path.join(root, 'server_local_files', client_name)
        files_in_client_folder = os.listdir(filepath)
        mes_split = message.split()
        if len(mes_split) > 1:
            client_files = mes_split[1].split(';')
            difference_files = list(set(client_files).symmetric_difference(set(files_in_client_folder)))
        else:
            difference_files = files_in_client_folder

        files_to_send = []
        for file in difference_files:
            f_size = os.path.getsize(os.path.join(filepath, file))
            filename_and_size = ':'.join([file, str(f_size)])
            files_to_send.append(filename_and_size)

        difference_files_and_sizes = ';'.join(files_to_send)
        message_to_send = ' '.join(['/readyforsendfiles', difference_files_and_sizes])
        await self._write_data_to_socket(writer, message_to_send)

        for file in difference_files:
            fullfilepath = os.path.join(filepath, file)
            with open(fullfilepath, 'rb') as file_to_send:
                filedata = file_to_send.read()
                await self._write_data_to_socket(writer, filedata)

            while True:
                data = await self._read_data_from_socket(reader)
                if data.decode() == 'next_file':
                    break

    async def _get_file_from_client(self, reader: StreamReader, writer: StreamWriter, message: str) -> bool:
        mes_details = message.strip().split()
        to_name = mes_details[1]
        file_details = mes_details[2].split(';')
        filepath = file_details[0]
        filesize = int(file_details[1])
        filename = os.path.basename(filepath)
        full_file_path = os.path.join(root, 'server_local_files', to_name, filename)
        if self._server_know_file_receiver(to_name):
            if not os.path.exists(full_file_path):
                if filesize <= self.limit_size_on_send_file:
                    message_to_send = f'/readytogetfile {filepath}'
                    await self._write_data_to_socket(writer, message_to_send)

                    chunk_size = 0
                    async with aiofiles.open(full_file_path, 'wb') as file:
                        while chunk_size < filesize:
                            data = await self._read_data_from_socket(reader)
                            await file.write(data)
                            chunk_size += len(data)
                    return True

                else:
                    message_to_send = f'/filesenderror file_size_is_more_than ' \
                                      f'{self.limit_size_on_send_file / 1048576}MB'
                    await self._write_data_to_socket(writer, message_to_send)
                    return False
            else:
                message_to_send = f'/filesenderror please_rename_file {filename}'
                await self._write_data_to_socket(writer, message_to_send)
                return False
        else:
            message_to_send = f'/filesenderror unknown_receiver {to_name}'
            await self._write_data_to_socket(writer, message_to_send)
            return False

    def _server_know_file_receiver(self, client_name: str) -> bool:
        if self.user_names.get(client_name):
            return bool(self.user_names.get(client_name))

    @staticmethod
    def _create_client_folder_if_not_exists(client_name: str) -> None:
        full_local_files_dir = os.path.join(root, 'server_local_files', client_name)
        if not os.path.exists(full_local_files_dir):
            os.mkdir(full_local_files_dir)

    async def _get_user_statuses(self, client_name: str) -> None:
        all_good = True
        if not self._message_counter_manager(client_name):
            await self._send_spam_warning_to_client(client_name)
            all_good = False
        if self.ban_list.get(client_name):
            await self._send_ban_warning_to_client(client_name)
            all_good = False
        if all_good:
            for writer in self.user_names[client_name]:
                await self._write_data_to_socket(writer, 'All good!')

    async def _send_spam_warning_to_client(self, client_name: str) -> None:
        current_time = datetime.now().timestamp()
        client_first_mes_time = self.first_message_client_time[client_name]
        waiting_time = int(self.timeout_for_limit_messages - (current_time - client_first_mes_time))
        for writer in self.user_names[client_name]:
            message_to_send = f'You have reached the limit in the number of messages. ' \
                              f'Please wait {waiting_time} seconds'
            await self._write_data_to_socket(writer, message_to_send)

    def _message_counter_manager(self, client_name: str) -> bool:
        self._message_counter_increment(client_name)

        if self.message_counter.get(client_name) > self.max_message_counter_per_client:
            current_time = datetime.now().timestamp()
            if current_time - self.first_message_client_time[client_name] <= self.timeout_for_limit_messages:
                return False
            else:
                del self.first_message_client_time[client_name]
                del self.message_counter[client_name]
                self._message_counter_increment(client_name)
        return True

    def _message_counter_increment(self, client_name: str) -> None:
        current_time = datetime.now().timestamp()
        if self.message_counter.get(client_name) is None:
            self.message_counter[client_name] = 1
            self.first_message_client_time[client_name] = current_time
        else:
            self.message_counter[client_name] += 1

    def _check_the_client_for_a_ban(self, name: str) -> bool:
        current_time = datetime.now().timestamp()
        if self.ban_list.get(name):
            if current_time - self.ban_list[name] < self.ban_timeout:
                return True
            else:
                del self.ban_list[name]
                del self.ban_counter[name]
        return False

    async def _ban_manager(self, message: str) -> None:
        data = message.split()
        name_for_ban = data[1]
        self._ban_counter_increment(name_for_ban)
        if self.ban_counter.get(name_for_ban, 0) >= 3:
            self._put_client_into_ban_list(name_for_ban)
            await self._send_ban_warning_to_client(name_for_ban)

    async def _send_ban_warning_to_client(self, client_name: str) -> None:
        current_time = datetime.now().timestamp()
        client_ban_time = self.ban_list[client_name]
        waiting_time = int(self.ban_timeout - (current_time - client_ban_time))
        for writer in self.user_names[client_name]:
            message_to_send = f'Other users ban you on this chat. Please wait {waiting_time} seconds'
            await self._write_data_to_socket(writer, message_to_send)

    def _ban_counter_increment(self, name: str) -> None:
        if self.ban_counter.get(name):
            self.ban_counter[name] += 1
        else:
            self.ban_counter[name] = 1

    def _put_client_into_ban_list(self, name: str) -> None:
        current_time = datetime.now().timestamp()
        if self.ban_list.get(name) is None:
            self.ban_list[name] = current_time

    async def _put_old_messages_to_writer(self, writer: StreamWriter, old_messages: list, name: str) -> None:
        if old_messages is not None:
            for from_user, to_user, msg in old_messages:
                message_to_send = f'{msg}\n'
                if to_user == name:
                    message_to_send = ': '.join([f'(Private){from_user}', f'{msg}\n'])
                elif to_user == 'ALL' and from_user != name:
                    message_to_send = ': '.join([from_user, f'{msg}\n'])
                elif to_user != 'ALL' and from_user == name:
                    message_to_send = ': '.join([f'@{to_user}', f'{msg}\n'])
                if message_to_send.strip('\n'):
                    await self._write_data_to_socket(writer, message_to_send)

    async def _get_client_name(self, reader: StreamReader) -> str:
        data = await self._read_data_from_socket(reader)
        message = data.decode().strip()
        name = message.split(':')[0]
        return name

    @staticmethod
    def _get_private_name_and_mes(data: str) -> Private:
        private_data = data.split()
        private_message = Private(
            name=private_data[0].strip().removeprefix('@'),
            data=' '.join(private_data[1:]).strip()
        )
        return private_message

    async def _notify_everyone(self, name: str) -> None:
        if self.user_names.get(name) is None:
            for client in self.clients:
                await self._write_data_to_socket(client, f'{name} connected!')

    def _put_user_into_user_names(self, writer: StreamWriter, username: str) -> None:
        if self.user_names.get(username) is None:
            self.user_names[username] = [writer]
        else:
            self.user_names[username].append(writer)

    def _put_writer_into_clients(self, writer: StreamWriter) -> None:
        if writer not in self.clients:
            self.clients.append(writer)

    async def _send_message_to_other_clients(self, writer: StreamWriter, message: str, from_name: str) -> None:
        message_to_send = ': '.join([from_name, message])
        if self.user_names.get(from_name):
            cl_writers = self.user_names[from_name]
            send_message = message_to_send.encode()
            for client in self.clients:
                if client not in cl_writers:
                    await self._write_data_to_socket(client, send_message)
            send_message = message.encode()
            for client in cl_writers:
                if client != writer:
                    await self._write_data_to_socket(client, send_message)

    async def _send_message_in_private_chats(self, from_name: str, to_name: str, pr_message: str, message: str,
                                             from_writer: StreamWriter) -> None:
        message_to_send = ': '.join([f'(Private){from_name}', pr_message])
        if self.user_names.get(to_name):
            send_message = message_to_send.encode()
            for writer in self.user_names[to_name]:
                await self._write_data_to_socket(writer, send_message)
        if self.user_names.get(from_name):
            send_message = message.encode()
            for writer in self.user_names[from_name]:
                if writer != from_writer:
                    await self._write_data_to_socket(writer, send_message)

    @staticmethod
    async def _read_data_from_socket(reader: StreamReader) -> bytes:
        return await reader.read(1024)

    @staticmethod
    async def _write_data_to_socket(writer: StreamWriter, message: str | bytes) -> None:
        if isinstance(message, str):
            message_for_send = message.encode()
        elif isinstance(message, bytes):
            message_for_send = message
        else:
            logger.warning('bad message type coming')
            return None
        writer.write(message_for_send)
        await writer.drain()

    async def run_server(self) -> None:
        chat_server = await asyncio.start_server(
            self._client_connected,
            self.host,
            self.port
        )
        address = chat_server.sockets[0].getsockname()
        logger.info(f'Serving on {address}')
        async with chat_server:
            await chat_server.serve_forever()

    def shutdown(self) -> None:
        for client in self.clients:
            client.write('Server is shutting down. Press Enter to exit.'.encode())
        self.loop.stop()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    server = Server(host='localhost', port=8000, loop=loop)
    try:
        asyncio.run(server.run_server())
    except KeyboardInterrupt:
        logger.warning('server is shutting down')
        server.shutdown()

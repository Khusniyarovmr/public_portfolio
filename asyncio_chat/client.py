import asyncio
import os
import sys
from asyncio.streams import StreamReader, StreamWriter
from dataclasses import dataclass, field
from typing import ClassVar

import aiofiles

from logger import logger

root = os.path.dirname(__file__)


@dataclass
class Client:
    user_name: ClassVar[str] = field(default='')
    local_client_folder_to_save_files: ClassVar[str] = field(default='')
    writer: ClassVar[StreamWriter] = field(default=None)
    reader: ClassVar[StreamReader] = field(default=None)
    host: str = field(default='localhost')
    port: int = field(default=8000)
    loop: asyncio.AbstractEventLoop = ''

    async def run_client(self) -> None:
        while self.user_name == '':
            self.user_name = input('For start chat, write your name: ').replace('\n', '')

        self._set_local_files_dir()

        cl_reader, cl_writer = await asyncio.open_connection(
            self.host,
            self.port
        )

        self._set_writer_and_reader(cl_reader, cl_writer)
        await self._send_welcome_message_to_server()

        try:
            await asyncio.gather(
                self._receive_messages(),
                self._start_client_cli()
            )
        except asyncio.exceptions.CancelledError:
            self.loop.close()
            sys.exit(1)

    def _set_local_files_dir(self) -> None:
        full_local_files_dir = os.path.join(root, 'client_local_files', self.user_name)
        if not os.path.exists(full_local_files_dir):
            os.mkdir(full_local_files_dir)
        self.local_client_folder_to_save_files = full_local_files_dir

    def _set_writer_and_reader(self, reader: StreamReader, writer: StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

    async def _write_data_to_socket(self, message: str | bytes) -> None:
        if isinstance(message, str):
            message_for_send = message.encode()
        elif isinstance(message, bytes):
            message_for_send = message
        else:
            return None
        self.writer.write(message_for_send)
        await self.writer.drain()

    async def _send_welcome_message_to_server(self) -> None:
        message_for_send = ': '.join([self.user_name, 'connected'])
        await self._write_data_to_socket(message_for_send)

    async def _receive_messages(self) -> None:
        message: str = ''
        while message != 'Server is shutting down. Press Enter to exit.':
            data = await self.reader.read(1024)
            message = data.decode().strip()
            if message:
                if message.startswith('/readytogetfile'):
                    await self._send_file_to_server(message)
                elif message.startswith('/readyforsendfiles'):
                    await self._get_files_from_server(message)
                else:
                    print(message)

        if self.loop.is_running():
            self.loop.close()
        self.shutdown()

    async def _start_client_cli(self) -> None:
        client_message: str = ''
        while client_message != '/exit':
            client_message = await asyncio.to_thread(input, "")
            if client_message:
                if client_message.startswith('/sendfile'):
                    await self._send_file_info_to_server(client_message)
                elif client_message.startswith('/getfiles'):
                    await self._send_filenames_to_server_for_sync()
                else:
                    await self._write_data_to_socket(client_message)

        if self.loop.is_running():
            self.loop.close()
        self.shutdown()

    async def _send_file_info_to_server(self, message: str) -> None:
        mes_split = message.split()
        if len(mes_split) > 2:
            filepath = mes_split[2]
            if os.path.exists(filepath):
                filesize = str(os.path.getsize(filepath))
                send_message = ';'.join([message, filesize])
                await self._write_data_to_socket(send_message)
            else:
                print('File not found!')
        else:
            print('Command have bad arguments')

    async def _get_files_from_server(self, message: str) -> None:
        mes_split = message.split()
        files = []
        if len(mes_split) > 1:
            files = mes_split[1].split(';')

        for file in files:
            file_detail = file.split(':')
            filename = file_detail[0]
            filesize = int(file_detail[1])
            full_file_path = os.path.join(self.local_client_folder_to_save_files, filename)
            chunk_size = 0
            async with aiofiles.open(full_file_path, 'wb') as get_file:
                while chunk_size < filesize:
                    data = await self.reader.read(1024)
                    await get_file.write(data)
                    chunk_size += len(data)

            await self._write_data_to_socket('next_file')

    async def _send_filenames_to_server_for_sync(self) -> None:
        current_files = ';'.join(os.listdir(self.local_client_folder_to_save_files))
        message = ' '.join(['/getfiles', current_files])
        await self._write_data_to_socket(message)

    async def _send_file_to_server(self, message: str) -> None:
        mes_details = message.strip().split()
        if len(mes_details) > 1:
            filepath = mes_details[1]
            if os.path.exists(filepath):
                async with aiofiles.open(filepath, 'rb') as file:
                    filedata = await file.read()
                await self._write_data_to_socket(filedata)
            else:
                print('File not found!')

    def shutdown(self) -> None:
        for task in asyncio.all_tasks():
            task.cancel()
        logger.info('Shutting down!')
        raise asyncio.exceptions.CancelledError


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    client = Client(host='localhost', port=8000, loop=loop)
    try:
        asyncio.run(client.run_client())
    except KeyboardInterrupt:
        logger.warning('KeyboardInterrupt detected! Shutting down!')
    except asyncio.exceptions.CancelledError as e:
        logger.warning(f'Emergency exit! Reason: {e}')
        sys.exit(1)
    except OSError as e:
        logger.warning('Server is offline')

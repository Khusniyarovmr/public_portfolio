from dataclasses import dataclass
import os
import stat
import shutil
from manual_exceptions import JobExecutionException
import urllib.request


@dataclass
class Tasks:

    @staticmethod
    def create_dir(pathname: str) -> None:
        try:
            os.mkdir(
                path=pathname,
                mode=stat.S_IRWXU,
                dir_fd=None
            )
        except Exception as e:
            raise JobExecutionException(e)

    @staticmethod
    def delete_dir(pathname: str) -> None:
        try:
            shutil.rmtree(
                path=pathname
            )
        except Exception as e:
            raise JobExecutionException(e)

    @staticmethod
    def create_file(pathname: str, filename: str) -> None:
        try:
            filepath = os.path.join(pathname, filename)
            with open(filepath, 'w') as file:
                file.write('')
        except Exception as e:
            raise JobExecutionException(e)

    @staticmethod
    def delete_file(pathname: str, filename: str) -> None:
        try:
            filepath = os.path.join(pathname, filename)
            os.remove(path=filepath)
        except Exception as e:
            raise JobExecutionException(e)

    @staticmethod
    def write_file(pathname: str, filename: str, text: str) -> None:
        try:
            filepath = os.path.join(pathname, filename)
            with open(filepath, 'a') as file:
                file.write(text + '\n')
        except Exception as e:
            raise JobExecutionException(e)

    @staticmethod
    def read_file(pathname: str, filename: str) -> None:
        try:
            filepath = os.path.join(pathname, filename)
            with open(filepath, 'r') as file:
                for line in file.readlines():
                    print(line)
            return
        except Exception as e:
            raise JobExecutionException(e)

    @staticmethod
    def get_request(url: str) -> None:
        try:
            new_url = url
            if 'http' not in new_url:
                new_url = f'https://{url}'
            with urllib.request.urlopen(new_url) as f:
                response = f.read()
                with open('response.txt', 'w') as file:
                    file.write(response.decode())
        except Exception as e:
            raise JobExecutionException(e)

    @staticmethod
    def analyze_response() -> None:
        try:
            with open('response.txt', 'r') as file:
                response = file.read()
            print(f'Analyzing response. Response get {len(response)} elements')
        except Exception as e:
            raise JobExecutionException(e)

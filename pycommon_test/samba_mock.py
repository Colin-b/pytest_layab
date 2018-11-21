import os.path
import re
from typing import List
from collections import namedtuple

# pysmb is not listed as dependency as it is optional and already provided by client in code
from smb.smb_structs import OperationFailure
from smb.base import SharedFile

SharedFileMock = namedtuple('SharedFileMock', ['filename'])


class TestConnection:
    """
    Mock a Samba Connection object.
    """

    should_connect = True
    stored_files = {}
    files_to_retrieve = {}

    def __init__(self, user_name, password, test_name, machine_name, *args, **kwargs):
        self.remote_name = machine_name

    def connect(self, *args):
        return self.should_connect

    def storeFile(self, share_drive_path: str, file_path: str, file) -> int:
        file_content = file.read()
        try:
            # Try to store string in order to compare it easily
            file_content = file_content.decode().replace('\r\n', '\n')
        except UnicodeDecodeError:
            pass  # Keep bytes when content is not str compatible (eg. Zip file)
        TestConnection.stored_files[(share_drive_path, file_path)] = file_content
        return 0

    def rename(self, share_drive_path: str, initial_file_path: str, new_file_path: str) -> None:
        TestConnection.stored_files[(share_drive_path, new_file_path)] = TestConnection.stored_files.pop((share_drive_path, initial_file_path), None)

    def retrieveFile(self, share_drive_path: str, file_path: str, file) -> (int, int):
        retrieved_file_content = TestConnection.files_to_retrieve.get((share_drive_path, file_path))
        if retrieved_file_content is not None:
            if os.path.isfile(retrieved_file_content):
                file.write(open(retrieved_file_content, mode='rb').read())
            else:
                file.write(str.encode(retrieved_file_content))
            return 0, 0
        raise OperationFailure(None, None)

    def listPath(self, service_name: str, path: str, pattern: str='*') -> List[SharedFile]:
        files_list = [
            SharedFileMock(os.path.basename(file_path))
            for _, file_path in TestConnection.stored_files
            if re.search(pattern, os.path.basename(file_path))
        ]
        if not files_list:
            raise OperationFailure(None, None)
        return files_list

    @classmethod
    def reset(cls):
        cls.should_connect = True
        cls.stored_files.clear()
        cls.files_to_retrieve.clear()


import smb.SMBConnection

smb.SMBConnection.SMBConnection = TestConnection

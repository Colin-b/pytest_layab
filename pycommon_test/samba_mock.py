class TestConnection:
    """
    Mock a Samba Connection object.
    """

    should_connect = True
    stored_files = {}
    files_to_retrieve = {}

    def __init__(self, *args, **kwargs):
        pass

    def connect(self, *args):
        return self.should_connect

    def storeFile(self, share_drive_path: str, file_path: str, file):
        TestConnection.stored_files[(share_drive_path, file_path)] = file.read().decode().replace('\r\n', '\n')

    def rename(self, share_drive_path: str, initial_file_path: str, new_file_path: str):
        TestConnection.stored_files[(share_drive_path, new_file_path)] = TestConnection.stored_files[(share_drive_path, initial_file_path)]

    def retrieveFile(self, share_drive_path: str, file_path: str, file):
        retrieved_file_path = TestConnection.files_to_retrieve.get((share_drive_path, file_path))
        if retrieved_file_path:
            with open(retrieved_file_path, 'rb') as file_to_retrieve:
                file.write(file_to_retrieve.read())

    @classmethod
    def reset(cls):
        cls.should_connect = True
        cls.stored_files.clear()
        cls.files_to_retrieve.clear()


import smb.SMBConnection

smb.SMBConnection.SMBConnection = TestConnection

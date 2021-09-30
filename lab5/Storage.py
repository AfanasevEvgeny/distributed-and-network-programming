import os


class Storage:
    def __init__(self, name):
        self.name = name
        self.filenames = []
        self.storage_directory = f'{name}_data'
        os.makedirs(self.storage_directory, exist_ok=True)

    def list_files(self):
        self.filenames = os.listdir(self.storage_directory)
        return self.filenames

    def is_in_storage(self, filename):
        self.filenames = os.listdir(self.storage_directory)
        return filename in self.filenames

    def send_file(self, filename, data: bytes):
        if self.is_in_storage(filename):
            return False
        else:
            if type(data) != bytes:
                data = data.data
            self.filenames.append(filename)
            with open(os.path.join(self.storage_directory, filename), 'wb') as file:
                file.write(data)
            return True

    def get_file(self, filename):
        if not self.is_in_storage(filename):
            return False
        else:
            with open(os.path.join(self.storage_directory, filename), 'rb') as file:
                data = file.read()
            if self.name == 'server':
                print(f"File send: {filename}")
            return data

    def delete_file(self, filename):
        if not self.is_in_storage(filename):
            if self.name == 'server':
                print(f"{filename} is not in server directory")
            return False
        else:
            os.remove(os.path.join(self.storage_directory, filename))
            if self.name == 'server':
                print(f"{filename} deleted")
            return True

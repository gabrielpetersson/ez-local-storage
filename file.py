import os
from abc import abstractmethod

import myturk
from myturk.constants import THREAD_STATUS_KEY


class File:

    def __init__(self, file_name):
        self._file_name = file_name
        self._file_directory = None  # can i force inheritors to define these?
        self._file_format = None
        self.sub_directories = []  # TODO: make private with setter

    @property
    def path(self):
        if self.file_directory is None: raise ValueError("directory of file is not set")
        if self.file_format is None: raise ValueError("format of file is not set")
        return os.path.join(self.file_directory, *self.sub_directories, self.file_name+self.file_format)

    @property
    def file_directory(self):
        return self._file_directory

    @property
    def file_format(self):
        return self._file_format

    @file_directory.setter
    def file_directory(self, directory):
        self._file_directory = directory

    @file_format.setter
    def file_format(self, format_):
        self._file_format = format_

    @property
    def file_name(self):
        return self._file_name

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, file):
        pass

    @abstractmethod
    def append_(self, file):
        pass


# TODO: might want to not be dependent of utils and load with json module
class JsonFile(File):
    JSON_FORMAT = '.json'

    def __init__(self, file_name):
        super().__init__(file_name)
        self.file_format = self.JSON_FORMAT

    def load(self):
        return myturk.utils.json_file_manager.load(self.path)

    def save(self, file):
        myturk.utils.json_file_manager.save(file, self.path)

    def append_(self, file):
        myturk.utils.json_file_manager.append_(file, self.path)


class TextFile(File):
    TEXT_FORMAT = '.txt'

    def __init__(self, file_name):
        super().__init__(file_name)
        self.file_format = self.TEXT_FORMAT

    def load(self):
        return open(self.path, 'r').read()

    def save(self, file):
        open(self.path, 'w').write(file)

    def append_(self, file):
        open(self.path, 'a+').write(file)


class MechanicalTurkStateFile(JsonFile):

    def __init__(self, file_name):
        super().__init__(file_name)

    @property
    def status(self):
        return self.load()[THREAD_STATUS_KEY]

    @status.setter
    def status(self, new_status):
        new_state = self.load()
        new_state[THREAD_STATUS_KEY] = new_status
        self.save(new_state)


class FileFactory:

    @staticmethod
    def _make_many(file_cls, names):
        return [file_cls(name) for name in names]

    @classmethod
    def txts(cls, file_names):
        return FileFactory._make_many(TextFile, file_names)

    @classmethod
    def jsons(cls, file_names):
        return FileFactory._make_many(JsonFile, file_names)
    
    @classmethod
    def txt(cls, file_name):
        return TextFile(file_name)

    @classmethod
    def json(cls, file_name):
        return JsonFile(file_name)

    @classmethod
    def state_file(cls, file_name):
        return MechanicalTurkStateFile(file_name)

    @classmethod
    def mock_file(cls, file_name):
        return File(file_name)

    @staticmethod
    def _listify(arg):
        return arg if isinstance(arg, list) else [arg]

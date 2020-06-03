import os
from abc import abstractmethod
from typing import List

import myturk
from myturk.local_storage.file import File
from myturk.local_storage.file import FileFactory
from myturk.constants import (
    LOCAL_STORAGE_NAME,
    LOCAL_STORAGE_JSON_FILE_NAMES,
    LOCAL_STORAGE_TEXT_FILE_NAMES,
    LOCAL_STORAGE_MTURK_THREAD_NAME,
    SHELL_FOLDER_NAME,
    TEMPORARY_STORAGE_NAME,
    THREAD_STATE_NAME
)


# TODO: add better interface and functionality
class Storage:
    @abstractmethod
    def add_file(self, file: File):
        pass

    @abstractmethod
    def __getattr__(self, file_name) -> File:
        pass


# TODO: add
class S3Storage(Storage):
    def add_file(self, file: File):
        pass

    def __getattr__(self, file_name) -> File:
        pass


# TODO: add better subdirectories functionality (not same namespace, etc, )
class LocalStorage(Storage):
    """creates a storage instance where only files added with add_file() can be
    reached as attributes. """
    __initialized = False
    __file_storage = '_file_storage'  # TODO: don't like referencing a function through string name. find fix
    __file_names = 'file_names'
    __sub_directory_names = 'sub_directory_names'
    __sub_directories = '_sub_directories'

    def __init__(self):
        self._path = os.path.join(os.getcwd(), LOCAL_STORAGE_NAME)
        self._file_storage = []  # TODO: build setter
        self._sub_directories = []
        self._file_factory = FileFactory()
        self.__initialized = True

    def __setattr__(self, key, item):
        if not self.__initialized:
            self.__dict__[key] = item
            return
        if self.__initialized and key in self.__file_names:
            self.__dict__[key].save(item)
        else:
            file = self._create_local_file(key)
            file.save(item)

    def __getattr__(self, file_name):
        file = self._create_local_file(file_name)
        return file

    def __str__(self):
        return self._path

    def _create_local_file(self, file_name):
        file = self._file_factory.json(file_name)
        self.add_file(file, sub_directories=[TEMPORARY_STORAGE_NAME])  # file is added as attr
        return self.__dict__[file_name]

    @property
    def file_names(self):
        return [file.file_name for file in self.__dict__[self.__file_storage]]

    @property
    def sub_directory_names(self):
        return [sub_directory.name for sub_directory in self.__dict__[self.__sub_directories]]

    @property
    def path(self):
        return self._path

    @property
    def file_local_storage_path(self):
        return os.path.join(self.local_storage_path, )

    def create(self, file_name):
        file = self._create_local_file(file_name)
        return file

    def add_sub_directory(self, sub_dir_name):
        sub_dir = self.SubDirectory(sub_dir_name)
        self.__dict__[sub_dir.name] = sub_dir
        self._sub_directories.append(sub_dir)

    def add_file(self, file: File, sub_directories: list = None):
        file.file_directory = self.path
        if sub_directories: file.sub_directories.extend(sub_directories)  # assign sub_dir to file
        self._file_storage.append(file)
        self.__dict__[file.file_name] = file

    def add_files(self, files: List[File], sub_directories: list = None):
        for file in files: self.add_file(file, sub_directories=sub_directories)

    class SubDirectory:

        def __init__(self, directory_name):
            self._directory_name = directory_name

        @property
        def name(self):
            return self._directory_name


# TODO: add JsonFile. and refactor class
class TaskShellStorage(Storage):
    PATH_SHELLS = os.path.join(os.getcwd(), SHELL_FOLDER_NAME)

    def __init__(self):
        self._file_path = self.PATH_SHELLS

    def load(self, file_name):
        return myturk.utils.json_file_manager.load(os.path.join(self._file_path, file_name))

    def add_file(self, file):
        raise NotImplementedError()


# setting up storage
file_factory = FileFactory()
local_storage = LocalStorage()
task_shell_storage = TaskShellStorage()
worker_performance_file = file_factory.json('worker_performance_file')
local_storage.add_file(worker_performance_file, sub_directories=['worker_performance'])

# TODO: sets up local storage. should move to some project specific module
# TODO: probably dont need any of this anymore
json_files = file_factory.jsons(LOCAL_STORAGE_JSON_FILE_NAMES)
text_files = file_factory.txts(LOCAL_STORAGE_TEXT_FILE_NAMES)

mturk_thread_file = file_factory.state_file(LOCAL_STORAGE_MTURK_THREAD_NAME)

local_storage.add_files(json_files, sub_directories=[TEMPORARY_STORAGE_NAME])
local_storage.add_files(text_files, sub_directories=[TEMPORARY_STORAGE_NAME])
local_storage.add_file(mturk_thread_file, sub_directories=[THREAD_STATE_NAME])

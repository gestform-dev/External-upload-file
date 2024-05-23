import os
import json
import logging


class FileUtils:
    @staticmethod
    def read_json_file(filepath):
        abs_file_path = FileUtils.get_abs_file_path(filepath)
        with open(abs_file_path) as json_data:
            data = json.load(json_data)
        return data

    @staticmethod
    def read_file(filepath):
        abs_file_path = FileUtils.get_abs_file_path(filepath)
        file_handle = open(abs_file_path)
        data = file_handle.read()
        file_handle.close()
        return data

    @staticmethod
    def get_abs_file_path(filepath):
        file_dir = os.path.dirname(__file__)
        return os.path.join(file_dir, filepath)


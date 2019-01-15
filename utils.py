import shutil
import requests
from PIL import Image
from io import BytesIO


def create_dir(path, parents=True):
    """
    create directory if dose not exists.
    :param path: Path: create dir path object
    :param parents: boolean: weather create parents dir, default is True.
    :return:
    """
    if not path.exists():
        path.mkdir(parents=parents)


def create_new_dir(path, parents=True):
    """
    create directory and delete it if exists.
    :param path: Path: create dir path object
    :param parents: boolean: weather create parents dir, default is True.
    :return:
    """
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=parents)

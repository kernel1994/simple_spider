import csv
import shutil
import logging
import pathlib


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


def msg_logging(level, msg, verbose=True):
    """
    logging and display message as specified level.
    :param level: logging level
    :param msg: message to log
    :param verbose: boolean: weather display message
    :return:
    """
    if verbose:
        print(msg)
    logging.log(level, msg)


def csv_writing(file_path: pathlib.Path, header: list, rows: list):
    """
    writing data to csv format file.
    :param file_path: pathlib.Path: csv file path object
    :param header: list[str]: string list of csv header name
    :param rows: list[dict]: dict list of data
    :return:
    """
    with file_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_reading(file_path: pathlib.Path) -> list:
    """
    read csv file.
    the fieldnames is omitted, the values in the first row of file f will be used as the fieldnames.
    :param file_path: pathlib.Path: csv file path object
    :return: list[dict]: dict list of data
    """
    with file_path.open('r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        return list(reader)

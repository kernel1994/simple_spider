import shutil
import pathlib
import requests
from itertools import repeat
from concurrent import futures

import utils


def downloader(save_path, url):
    image_name = url.split('/')[-1].split('?')[0]
    image_path = save_path.joinpath(image_name)

    print('downloading {}'.format(image_name))

    r = requests.get(url, stream=True)
    with image_path.open('wb') as o:
        shutil.copyfileobj(r.raw, o)


def task_many(save_path, urls, n_workers):
    """
    download images from urls concurrently.
    :param dir: pathlib.Path: where to save images
    :param image_urls: iterable: image urls
    :param n_workers: int: number of threads
    """
    workers = min(n_workers, len(urls))

    with futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(downloader, repeat(save_path), urls)

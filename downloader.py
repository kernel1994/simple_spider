import pathlib
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from concurrent import futures


def downloader(save_path, url):
    image_name = url.split('/')[-1].split('?')[0]

    print('downloading {}'.format(image_name))

    r = requests.get(url)
    image = Image.open(BytesIO(r.content))
    image.save(save_path.joinpath(image_name))


def task_one(save_path, urls):
    for url in urls:
        downloader(save_path, url)


def task_many(save_path, urls, n_workers):
    """
    download images from urls concurrently.
    :param dir: pathlib.Path: where to save images
    :param image_urls: iterable: image urls
    :param n_workers: int: number of threads
    """
    workers = min(n_workers, len(urls))

    # divide all urls into n_workers group for every thread
    url_group = np.array_split(urls, workers)

    with futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for i in range(workers):
            executor.submit(task_one, save_path, url_group[i])

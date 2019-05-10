from itertools import repeat
from concurrent import futures
from urllib.request import urlretrieve


def downloader(url, save_path):
    image_name = url.split('/')[-1].split('?')[0]
    image_path = save_path.joinpath(image_name)

    print('downloading {}'.format(image_name))

    urlretrieve(url, image_path)


def task_many(urls, save_path, n_workers):
    """
    download images from urls concurrently.
    :param urls: iterable: image urls
    :param save_path: pathlib.Path: where to save images
    :param n_workers: int: number of threads
    """
    workers = max(min(n_workers, len(urls)), 1)

    with futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(downloader, urls, repeat(save_path, times=len(urls)), timeout=60)

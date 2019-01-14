import shutil
import requests
from PIL import Image
from io import BytesIO


def download_image(dir, image_urls):
    """
    download image from urls.
    :param dir: pathlib.Path: where to save images
    :param image_urls: iterable: image urls
    """
    for image_url in image_urls:
        image_name = image_url.split('/')[-1].split('?')[0]
        image_save_path = dir.joinpath(image_name)

        print('downloading {} ...'.format(image_name))

        r = requests.get(image_url)
        image = Image.open(BytesIO(r.content)).convert('RGB')
        image.save(image_save_path)


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

import csv
import time
import logging
import pathlib
import requests
import pandas as pd

import utils
import downloader
import weibo_config as wc


class WeiboSpider:
    def __init__(self, config, request_headers, reentry=False, override=False):
        self.config = config
        self.request_headers = request_headers
        self.reentry = reentry

        self.main_path = pathlib.Path(config.main_path)
        if override:
            utils.create_new_dir(self.main_path)
        else:
            utils.create_dir(self.main_path)

        self.images_path = self.main_path.joinpath(config.images_path)
        if override:
            utils.create_new_dir(self.images_path)
        else:
            utils.create_dir(self.images_path)

        self.csv_file = self.main_path.joinpath(config.csv_file)
        self.log_file = self.main_path.joinpath(config.log_file)
        self.stop_file = self.main_path.joinpath(config.stop_file)

        # init logging config
        logging.basicConfig(level=logging.INFO,
                            filename=self.log_file,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s    %(levelname)s    %(filename)s[line:%(lineno)d]    %(message)s')

    def grab_comment_hotflow(self, mid=0):
        """
        Grab comments of one weibo order by hot.
        NOTE: This can only get the first level comments
        :param mid: int, which post want to grab
        :return:
        """
        csv_header = ['review_id', 'user_id', 'pic_pid', 'pic_url',
                      'user_profile_url', 'created_at', 'like_counts',
                      'user_image', 'user_avatar_hd', 'user_name',
                      'user_description', 'comment']
        f_csv = self.csv_file.open('a', newline='', encoding='utf-8')
        writer = csv.DictWriter(f_csv, fieldnames=csv_header)

        if self.reentry:
            row = utils.csv_reading(self.stop_file)[0]
            max_id = row['max_id']
            max_id_type = row['max_id_type']
        else:
            writer.writeheader()

            # first shoot to get the first max_id
            first_hotflow_url = self.config.init_hotflow_tmp.format(mid=mid)
            # response JSON data
            rj = requests.get(first_hotflow_url, headers=self.request_headers).json()
            # get the max_id to access next page
            max_id = rj['data']['max_id']
            max_id_type = rj['data']['max_id_type']

            # the first url (without max_id) also carry data
            # parse data item and write csv
            for data_item in rj['data']['data']:
                writer.writerow(self._parse_data_item(data_item))

        tris = 0
        while max_id:
            try:
                next_hotflow_url = wc.next_hotflow_tmp.format(mid=mid, max_id=max_id, max_id_type=max_id_type)
                utils.msg_logging(logging.INFO, 'Try get {}'.format(next_hotflow_url), verbose=False)
                rj = requests.get(next_hotflow_url, headers=self.request_headers).json()

                msg = 'max_id {} -> {}'.format(max_id, 'ok' if rj['ok'] else 'error')
                utils.msg_logging(logging.INFO, msg)

                # get next max_id
                max_id = rj['data']['max_id']
                # get next max_id_type
                max_id_type = rj['data']['max_id_type']

                # parse data item and write csv
                for data_item in rj['data']['data']:
                    writer.writerow(self._parse_data_item(data_item))

                time.sleep(self.config.sleep_per_step)

                # reset tries to 0 after request successfully
                tris = 0
            except Exception as e:
                if tris >= self.config.try_times:
                    msg = 'Exhausted. Try {} times. End in {}. With max_id={}'.format(self.config.try_times,
                                                                                      next_hotflow_url, max_id)
                    utils.msg_logging(logging.ERROR, msg)
                    utils.csv_writing(self.stop_file, header=['max_id', 'max_id_type'],
                                      rows=[{'max_id': max_id, 'max_id_type': max_id_type}])

                    f_csv.close()
                    break

                tris += 1

                msg = '{} error happened! The {} time(s) try. Sleep a while.'.format(e, tris)
                utils.msg_logging(logging.WARNING, msg)

                time.sleep(self.config.sleep_baned)

    def download_pic(self):
        # download image via crawled information
        weibo_df = pd.read_csv(self.csv_file)
        urls = weibo_df[weibo_df['pic_url'].notnull()]['pic_url']
        urls = pd.unique(urls)
        downloader.task_many(urls, self.images_path, n_workers=self.config.n_download_workers)

    def _parse_data_item(self, item):
        """
        parse json data item.
        :param item: json data item
        :return: dict: parsed data dict
        """
        # comment
        review_id = item['id']
        created_at = item['created_at']
        like_counts = item['like_count']
        comment = item['text']

        # user
        user_id = item['user']['id']
        user_name = item['user']['screen_name']
        user_image = item['user']['profile_image_url']
        user_profile_url = item['user']['profile_url']
        user_description = item['user']['description']
        user_avatar_hd = item['user']['avatar_hd']

        # picture
        pic_pid = item.get('pic', {}).get('pid', None)
        pic_url = item.get('pic', {}).get('large', {}).get('url', None)

        return {'review_id': review_id, 'user_id': user_id, 'pic_pid': pic_pid, 'pic_url': pic_url,
                'user_profile_url': user_profile_url, 'created_at': created_at, 'like_counts': like_counts,
                'user_image': user_image, 'user_avatar_hd': user_avatar_hd, 'user_name': user_name,
                'user_description': user_description, 'comment': comment}


if __name__ == '__main__':
    headers = wc.headers

    weibo_spider = WeiboSpider(wc, headers, reentry=False, override=True)
    weibo_spider.grab_comment_hotflow(wc.mid)
    weibo_spider.download_pic()

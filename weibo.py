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

        self.image_path = self.main_path.joinpath(config.image_path)
        utils.create_dir(self.image_path)
        self.csv_file = self.main_path.joinpath(config.csv_path)
        self.log_file = self.main_path.joinpath(config.log_path)
        self.stop_file = self.main_path.joinpath(config.stop_path)

        logging.basicConfig(level=logging.DEBUG,
                            filename=self.log_file,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(asctime)s    %(levelname)s    %(filename)s[line:%(lineno)d]    %(message)s')

    def grab_comment_hotflow(self, mid=0):
        if self.reentry:
            with self.stop_file.open('r') as sfr:
                max_id = int(sfr.readline().split('=')[-1])
                print(max_id)
        else:
            # first shoot to get the first max_id
            first_hotflow_url = self.config.init_hotflow_tmp.format(mid=mid)
            # response JSON data
            rj = requests.get(first_hotflow_url, headers=self.request_headers).json()
            # get the max_id to access next page
            max_id = rj['data']['max_id']

        csv_header = ['review_id', 'user_id', 'pic_pid', 'pic_url',
                      'user_profile_url', 'created_at', 'like_counts',
                      'user_image', 'user_avatar_hd', 'user_name',
                      'user_description', 'comment']

        with self.csv_file.open('a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_header)
            writer.writeheader()

            tris = 0
            while max_id:
                try:
                    # initial max_id_type is 0
                    max_id_type = 0
                    next_hotflow_url = wc.next_hotflow_tmp.format(mid=mid, max_id=max_id, max_id_type=max_id_type)
                    logging.info('Try get {}'.format(next_hotflow_url))
                    rj = requests.get(next_hotflow_url, headers=self.request_headers).json()

                    # change max_id_type if get nothing back, and re-access
                    # I do not know the rule of max_id_type is 1 or 0
                    if not rj['ok']:
                        max_id_type = 1
                        next_hotflow_url = wc.next_hotflow_tmp.format(mid=mid, max_id=max_id, max_id_type=max_id_type)
                        logging.warning('Change max_id_type, re-try {}'.format(next_hotflow_url))
                        rj = requests.get(next_hotflow_url, headers=self.request_headers).json()

                    msg = 'max_id {} -> {}'.format(max_id, 'ok' if rj['ok'] else 'error')
                    print(msg)
                    logging.info(msg)

                    # get next max_id
                    max_id = rj['data']['max_id']

                    data = rj['data']['data']

                    for d in data:
                        # comment
                        review_id = d['id']
                        created_at = d['created_at']
                        like_counts = d['like_count']
                        comment = d['text']

                        # user
                        user_id = d['user']['id']
                        user_name = d['user']['screen_name']
                        user_image = d['user']['profile_image_url']
                        user_profile_url = d['user']['profile_url']
                        user_description = d['user']['description']
                        user_avatar_hd = d['user']['avatar_hd']

                        # picture
                        pic_pid = d.get('pic', {}).get('pid', None)
                        pic_url = d.get('pic', {}).get('large', {}).get('url', None)

                        writer.writerow({'review_id': review_id, 'user_id': user_id, 'pic_pid': pic_pid, 'pic_url': pic_url,
                                         'user_profile_url': user_profile_url, 'created_at': created_at,
                                         'like_counts': like_counts,
                                         'user_image': user_image, 'user_avatar_hd': user_avatar_hd, 'user_name': user_name,
                                         'user_description': user_description, 'comment': comment})

                    time.sleep(self.config.sleep_per_step)
                except Exception as e:
                    if tris >= self.config.try_times:
                        msg = 'Exhausted. Try {} times. End in {}. With max_id={}'.format(self.config.try_times,
                                                                                          next_hotflow_url, max_id)
                        print(msg)
                        with self.stop_file.open('w', encoding='utf-8') as sfw:
                            sfw.write(msg)
                        break

                    tris += 1
                    msg = '{} error happened! The {} time(s) try. With max_id={}'.format(e, tris, max_id)
                    print(msg)
                    logging.warning(msg)
                    time.sleep(self.config.sleep_baned)

    def download_pic(self):
        # download image via crawled information
        weibo_df = pd.read_csv(self.csv_file)
        urls = weibo_df[weibo_df['pic_url'].notnull()]['pic_url']
        downloader.task_many(self.image_path, urls, n_workers=self.config.n_download_workers)

    def grab_comment(self, post_id):
        # NOTE: DEPRECATED: this api can only crawl 100 pages, First consider using grab_comment_hotflow()
        # single_post_id find in:
        # m.weibo.cn/status/{post_id}
        # m.weibo.cn/statuses/show?id={post_id}

        # first shoot to get page information
        single_weibo_url = self.config.comments_tmp.format(id=post_id, page=1)
        # response JSON data
        rj = requests.get(single_weibo_url, headers=self.request_headers).json()
        # get the max number of pages
        n_max_page = rj['data']['max']

        csv_header = ['review_id', 'user_id', 'pic_pid', 'pic_url',
                      'user_profile_url', 'created_at', 'like_counts',
                      'user_image', 'user_name', 'comment']

        with self.csv_file.open('a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_header)
            writer.writeheader()

            for i in range(1, n_max_page):
                single_weibo_url = self.config.comments_tmp.format(id=post_id, page=i)

                rj = requests.get(single_weibo_url, headers=self.request_headers).json()
                print('page {} -> {}'.format(i, rj['msg']))
                data = rj['data']['data']

                for d in data:
                    # comment
                    review_id = d['id']
                    created_at = d['created_at']
                    like_counts = d['like_counts']
                    comment = d['text']

                    # user
                    user_id = d['user']['id']
                    user_name = d['user']['screen_name']
                    user_image = d['user']['profile_image_url']
                    user_profile_url = d['user']['profile_url']

                    # picture
                    pic_pid = d.get('pic', {}).get('pid', None)
                    pic_url = d.get('pic', {}).get('large', {}).get('url', None)

                    writer.writerow({'review_id': review_id, 'user_id': user_id, 'pic_pid': pic_pid, 'pic_url': pic_url,
                                     'user_profile_url': user_profile_url, 'created_at': created_at, 'like_counts': like_counts,
                                     'user_image': user_image, 'user_name': user_name, 'comment': comment})

                time.sleep(self.config.sleep_per_step)


if __name__ == '__main__':
    headers = wc.headers

    weibo_spider = WeiboSpider(wc, headers, reentry=False, override=False)
    weibo_spider.grab_comment_hotflow(wc.mid)
    weibo_spider.download_pic()

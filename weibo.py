"""
Weibo API Templates

single post with comments
https://m.weibo.cn/api/comments/show?id={id}&page={page}

posts for a user
https://m.weibo.cn/api/container/getIndex?containerid={oid}&type=uid&value={uid}&page={page}

user index
https://m.weibo.cn/api/container/getIndex?type=uid&value={usr_id}
"""
import time
import pathlib
import requests
import pandas as pd

import utils


def grab_comment(csv_file):
    # the weibo id which want to grab
    single_weibo_id = 'GuBb7tcdA'
    cookie = 'YOUR COOKIE HERE'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    headers = {
        'cookie': cookie,
        'user-agent': user_agent
    }

    single_weibo_url_tmp = 'https://m.weibo.cn/api/comments/show?id={id}&page={page}'

    # first shoot to get page information
    single_weibo_url = single_weibo_url_tmp.format(id=single_weibo_id, page=1)
    # response JSON data
    rj = requests.get(single_weibo_url, headers=headers).json()
    # get the max number of pages
    n_max_page = rj['data']['max']

    with csv_file.open('a', encoding='utf-8') as f:
        for i in range(1, n_max_page):
            single_weibo_url = single_weibo_url_tmp.format(id=single_weibo_id, page=i)

            rj = requests.get(single_weibo_url, headers=headers).json()
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

                f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(
                    review_id,user_id,pic_pid,pic_url,user_profile_url,
                    created_at,like_counts,user_image,user_name,comment)
                )

            time.sleep(1)


if __name__ == '__main__':
    override = True

    # where to save crawled csv file
    csv_file = pathlib.Path('weibo.csv')
    # where to save downloaded images
    img_dir = pathlib.Path('images')
    if override:
        with csv_file.open('w', encoding='utf-8') as f:
            f.write('review_id,user_id,pic_pid,pic_url,user_profile_url,created_at,like_counts,user_image,user_name,comment\n')

        utils.create_new_dir(img_dir)
    else:
        utils.create_dir(img_dir)

    # Crawl comments of one post
    grab_comment(csv_file)

    # download image via crawled information
    weibo_df = pd.read_csv(csv_file)
    urls = weibo_df[weibo_df['pic_url'] != 'None']['pic_url']
    utils.download_image(img_dir, urls)

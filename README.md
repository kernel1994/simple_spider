# simple_spider
Some simple python spiders for learning.

weibo.py crawl weibo comments and download images.

## Weibo API Templates

- comments hotflow
    - first level
        - https://m.weibo.cn/comments/hotflow?id={mid}&mid={mid}&max_id_type={0|1}  # init url
        - https://m.weibo.cn/comments/hotflow?id={mid}&mid={mid}&max_id={max_id}&max_id_type={0|1}  # next page url
    - second level
        - https://m.weibo.cn/comments/hotFlowChild?cid={cid}&max_id=0&max_id_type={0|1}  # init url
        - https://m.weibo.cn/comments/hotFlowChild?cid={cid}&max_id={max_id}&max_id_type={0|1}  # next page url

- single post with comments  # DEPRECATED
    - NOTE: this api can only crawl 100 pages, First consider using hotflow
    - https://m.weibo.cn/api/comments/show?id={id}&page={page}

- posts for a user
    - https://m.weibo.cn/api/container/getIndex?containerid={oid}&type=uid&value={uid}&page={page}

- user index
    - https://m.weibo.cn/api/container/getIndex?type=uid&value={usr_id}

## How to run
Set `mid` and paste `cookie` and `user_agent` into `weibo_config.py`. And adapt other configurations.

Then run `python weibo.py`

If you get `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` error,
you should login and recopy the cookie, or change account.

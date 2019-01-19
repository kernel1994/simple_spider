# API url templates
# init hotflow url template. Used to get the first max_id
init_hotflow_tmp = 'https://m.weibo.cn/comments/hotflow?id={mid}&mid={mid}&max_id_type=0'
# next hotflow url template, use max_id to request next data
next_hotflow_tmp = 'https://m.weibo.cn/comments/hotflow?id={mid}&mid={mid}&max_id={max_id}&max_id_type={max_id_type}'
# comments url of single post. NOTE: this API can only access 100 pages
comments_tmp = 'https://m.weibo.cn/api/comments/show?id={id}&page={page}'

# request headers
# cookie
cookie = 'YOUR COOKIE HERE'
# user agent
user_agent = 'YOUR UA HERE'
headers = {
    'cookie': cookie,
    'user-agent': user_agent
}

# pause time
# sleep seconds of every request
sleep_per_step = 1
# sleep seconds when baned
sleep_baned = 5 * 60

# number of downloader workers
n_download_workers = 32
# try times when exception raised
try_times = 5

# work file and path
# working path
main_path = 'weibo_save/'
# downloaded images path
images_path = 'images/'
# csv file name
csv_file = 'weibo.csv'
# log file name
log_file = 'weibo.log'
# pause log file name
stop_file = 'stop.csv'

# weibo hotflow mid need to be crawled.
# Find it use Chrome Dev Tool m.weibo.cn/comments/hotflow?id={mid}&mid={mid}
# or m.weibo.cn/detail/{mid}
mid = 0

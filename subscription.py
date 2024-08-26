import requests
import json
from utils.get_by_api import get_subs
from utils.cookie import get_lofter_authkey
import os
import time

def save_subs(authkey, save_path='./results', sleep_time=0.1):
    '''
    保存订阅列表

    Args:
    authkey: 登录信息(LOFTER-PHONE-LOGIN-AUTH)
    save_path: 保存路径，默认为'./results'
    sleep_time: 请求间隔，默认为0.2秒
    '''

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    start = 0 # 起始位置
    data = get_subs(authkey, start)['data']
    offset = data['offset'] # 结束位置
    subscribeCollectionCount = data['subscribeCollectionCount']
    collections = data['collections']

    if subscribeCollectionCount > 10:
        for i in range(10, subscribeCollectionCount, 10):
            time.sleep(sleep_time)
            data = get_subs(authkey, i)['data']
            collections += data['collections']

    with open(f'{save_path}/subscription.json', 'w', encoding='utf-8') as f:
        json.dump(collections, f, ensure_ascii=False, indent=4)
        print(f'订阅信息保存至 {save_path}/subscription.json')


if __name__ == '__main__':
    # 保存路径
    save_path = './results/'

    # 需要登录信息(LOFTER-PHONE-LOGIN-AUTH)
    # 可自行填写或者自动获取（需要浏览器已经登陆lofter）
    authkey = get_lofter_authkey(browser='default')  # 自动获取
    # authkey = 'your_authkey_here' # 手动填写

    save_subs(authkey, save_path, sleep_time=0.1)
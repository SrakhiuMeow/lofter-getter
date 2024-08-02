from utils.get_by_api import get_collection_list, get_collection
import json
import time
import os

if __name__ == '__main__':

    save_path = './results/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    collection_id = 0
    blog_id = 0

    sleep_time = 0.2

    collection = get_collection_list(collection_id, blog_id, 0)

    postCount = collection['collection']['postCount']

    collection_list = []
    for i in range(0, postCount, 15):
        time.sleep(sleep_time)
        collection_list += get_collection_list(collection_id, blog_id, i)['items']

    for c in collection_list:
        print(c['post']['title'])
        with open(f'{save_path}{c["post"]["title"].replace('/', '_')}.html', 'w', encoding='utf-8') as f:
            f.write(c['post']['content'])
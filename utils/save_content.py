import requests
import json
from utils.get_by_api import get_subs, get_collection_list
from utils.get_by_api import get_post
from utils.proc_str import make_valid_filename, escape_for_url, html2md
from utils.proc_img import replace_img_url, download_img
from utils.cookie import get_lofter_authkey
import os
import time

def save_single_post(blog_id, post_id, save_path='./results', rewrite=False):
    save_path = './results'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # 博客ID和文章ID，可根据APP端的分享链接获取
    blog_id = 0
    post_id = 0
    
    posts = get_post(blog_id, post_id)['posts']
    for i in posts:
        print(i['post']['title'])
        with open(f'{save_path}/{i["post"]["title"].replace("/", "_")}.html', 'w', encoding='utf-8') as f:
            f.write(i['post']['content'])


def save_single_collection(collection_id, save_path='./results', save_img=True,rewrite=False, sleep_time=0.2):
    '''
    保存合集内容

    Args:
    collection_id: 合集ID
    save_path: 保存路径，默认为'./results'
    rewrite: 是否覆盖已存在的文件，默认为False
    sleep_time: 请求间隔，默认为0.2秒
    '''
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    collection = get_collection_list(collection_id,  0)

    post_count = collection['collection']['postCount']
    collection_name = collection['collection']['name']
    print(f'合集名：{collection_name}，文章数量：{post_count}')


    collection_list = []
    for i in range(0, post_count, 15):
        time.sleep(sleep_time)
        collection_list += get_collection_list(collection_id,  i)['items']

    collection_path = f'{save_path}/{collection_name}'
    if not os.path.exists(collection_path):
        os.makedirs(collection_path)

    img_path = f'{collection_path}/images'
    if save_img and not os.path.exists(img_path):
        os.makedirs(img_path)

    # with open(f'{save_path}/{collection_name}.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(collection_list, ensure_ascii=False))

    title_list = []
    title_url_list = []
    # 保存合集目录
    with open(f'{save_path}/{collection_name}.md', 'w', encoding='utf-8') as f:
        f.write(f'### 合集名：{collection_name}，文章数量：{post_count}\n')
        for i, c in enumerate(collection_list):
            title = c['post']['title']

            # 调整标题格式
            title = make_valid_filename(title)
            title_url = escape_for_url(title)

            title_list.append(title)
            title_url_list.append(title_url)

            if os.path.exists(f'{collection_path}/{i+1}-{title}.md'):
                f.write(f'- [{title}]({collection_name}/{i+1}-{title_url}.md)\n')
            else:
                f.write(f'- **[{title}]({collection_name}/{i+1}-{title_url}.md)**\n')
            

    # 保存文章内容
    for i, c in enumerate(collection_list):
        title = title_list[i]
        print(title)

        # 如果文件已存在，则跳过
        if not rewrite:
            if os.path.exists(f'{collection_path}/{i+1}-{title}.md'):
                continue

        # 保存文章内容
        with open(f'{collection_path}/{i+1}-{title}.md', 'w', encoding='utf-8') as t:
            t.write(f'## {title}\n')
            content = c['post']['content']

            # 转换HTML为Markdown
            content = html2md(content)
            
            # 保存图片并替换URL
            if save_img:
                content, img_list = replace_img_url(content, cvt2local=True)
                download_img(img_list, img_path)

            t.write(content)

            if i > 0:
                t.write(f'\n\n上一篇： [{title_list[i-1]}](./{i}-{title_url_list[i-1]}.md)\n')
            if i < len(title_list) - 1:
                t.write(f'\n\n下一篇： [{title_list[i+1]}](./{i+2}-{title_url_list[i+1]}.md)\n')


def save_all_collections(authkey, save_path='./results', save_img=True, rewrite=False, sleep_time=0.2):
    '''
    保存订阅中的所有合集内容

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

    for c in collections:
        collection_id = c['collectionId']
        collection_name = c['name']
        # print(f'合集名：{collection_name}，合集ID：{collection_id}')
        save_single_collection(collection_id, save_path, save_img=save_img,
                               rewrite=rewrite, sleep_time=sleep_time)


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


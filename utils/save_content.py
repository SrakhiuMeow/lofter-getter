import requests
import json
from utils.get_by_api import get_subs, get_collection_list, get_history
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


def save_single_collection(collection_id, save_path='./results', save_img=True, limit_once=50, rewrite=False, sleep_time=0.2):
    '''
    保存合集内容

    Args:
    collection_id: 合集ID
    save_path: 保存路径，默认为'./results'
    limit_once: 每次获取文章数量，默认为50
    rewrite: 是否覆盖已存在的文件，默认为False
    sleep_time: 请求间隔，默认为0.2秒
    '''
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    collection = get_collection_list(collection_id,  0, limit_once)

    post_count = collection['collection']['postCount']
    collection_name = collection['collection']['name']
    collection_tags = collection['collection']['tags'].split(',')
    collection_description = collection['collection']['description']
    print(f'合集名：{collection_name}，文章数量：{post_count}')


    collection_list = []
    for i in range(0, post_count, limit_once):
        time.sleep(sleep_time)
        collection_list += get_collection_list(collection_id,  i, limit_once)['items']

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
        f.write(f'### {collection_name}\n')
        f.write(collection_description + '\n\n')
        f.write('---\n')
        f.write(f'#### 目录(共{post_count}篇)\n')
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
        f.write('---\n')
        f.write('#### 标签\n')
        for tag in collection_tags:
            f.write(f'[{tag}](https://www.lofter.com/tag/{tag})  ')

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
            t.write(f'## [{title}]({c['post']['blogPageUrl']})\n')
            content = c['post']['content']

            # 转换HTML为Markdown
            content = html2md(content)
            
            # 保存图片并替换URL
            if save_img:
                content, img_list = replace_img_url(content, cvt2local=True)
                download_img(img_list, img_path)

            t.write(content)

            t.write('\n\n---\n')
            t.write(f'#### 热门评论\n')
            for comment in c['hotComments']:
                nickname = comment['publisherMainBlogInfo']['blogNickName']
                bloghome = comment['publisherMainBlogInfo']['homePageUrl']
                t.write(f'- [{nickname}]({bloghome}):  {comment["content"]}\n')
            
            t.write('\n\n---\n')
            t.write(f'#### 标签\n')
            for tag in c['post']['tagList']:
                t.write(f'[{tag}](https://www.lofter.com/tag/{tag})  ')

            t.write('\n\n---\n')
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


def save_subs(authkey, save_path='./results', sleep_time=0.1, limit_once=50):
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

    if subscribeCollectionCount > limit_once:
        for i in range(limit_once, subscribeCollectionCount, limit_once):
            time.sleep(sleep_time)
            data = get_subs(authkey, i, limit_once)['data']
            collections += data['collections']

    for c in collections:
        collection_id = c['collectionId']
        if not c['valid']:
            print(f'合集{collection_id}已失效')
            continue
        collection_name = c['name']
        print(f'合集名：{collection_name}，合集ID：{collection_id}')

    with open(f'{save_path}/subscription.json', 'w', encoding='utf-8') as f:
        json.dump(collections, f, ensure_ascii=False, indent=4)
        print(f'订阅信息保存至 {save_path}/subscription.json')

def save_history(authkey, blogdomain, save_path='./results', sleep_time=0.1, limit_once=50, save_img=True):
    '''
    保存历史记录

    Args:
    authkey: 登录信息(LOFTER-PHONE-LOGIN-AUTH)
    save_path: 保存路径，默认为'./results'
    sleep_time: 请求间隔，默认为0.2秒
    '''

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if not os.path.exists(save_path+'/history'):
        os.makedirs(save_path+'/history')

    img_path = save_path+'/history/images'
    if save_img and not os.path.exists(img_path):
        os.makedirs(img_path)

    start = 0 # 起始位置
    data = get_history(authkey, blogdomain, start, limit_once)
    historyCount = data['count']
    posts = data['items']

    if historyCount > limit_once:
        for i in range(limit_once, historyCount, limit_once):
            time.sleep(sleep_time)
            data = get_history(authkey, blogdomain, i, limit_once)
            posts += data['items']

    for p in posts:
        p = p['post']
        post_id = p['id']
        if p['blogId'] == 0:
            continue
        try:
            post_title = p['title']
            post_title = make_valid_filename(post_title)
        except:
            continue
        if len(post_title) == 0:
            post_title = '无标题'+str(post_id)
        print(f'文章标题：{post_title}，文章ID：{post_id}')
        with open(f'{save_path}/history/{post_title}.md', 'w', encoding='utf-8') as t:
            t.write(f'## [{post_title}]({p['blogPageUrl']})\n')
            content = p['content']
            # 转换HTML为Markdown
            content = html2md(content)

            if save_img:
                content, img_list = replace_img_url(content, cvt2local=True)
                download_img(img_list, img_path)
            
            t.write(content)

            t.write('\n\n---\n')
            t.write(f'#### 标签\n')
            for tag in p['tagList']:
                t.write(f'[{tag}](https://www.lofter.com/tag/{tag})  ')
            

    with open(f'{save_path}/history.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
        print(f'历史记录保存至 {save_path}/history.json')
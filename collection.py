from utils.get_by_api import get_collection_list, get_collection
import json
import time
import os
import re
from utils.string_proc import make_valid_filename, escape_for_url, html2md
from utils.image_proc import replace_img_url, download_img



def save_collection(collection_id, save_img=True, save_path='./results', rewrite=False, sleep_time=0.2):
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

        if i < 107:
            continue

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
                t.write(f'\n下一篇： [{title_list[i+1]}](./{i+2}-{title_url_list[i+1]}.md)\n')



if __name__ == '__main__':
    # 保存路径
    save_path = './results'

    # 合集ID，可根据APP端的分享链接获取
    collection_id = 20460170

    # 保存合集
    save_collection(collection_id, save_path, rewrite=True)
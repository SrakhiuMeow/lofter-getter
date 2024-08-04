from utils.get_by_api import get_collection_list, get_collection
import json
import time
import os
import re



def save_collection(collection_id, save_path='./results', sleep_time=0.2):
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

    # with open(f'{save_path}/{collection_name}.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(collection_list, ensure_ascii=False))

    title_list = []
    with open(f'{save_path}/{collection_name}.md', 'w', encoding='utf-8') as f:
        f.write(f'### 合集名：{collection_name}，文章数量：{post_count}\n')
        for c in collection_list:
            title = c['post']['title']
            title = title.replace('/', '_')
            f.write(f'- [{title}]({collection_name}/{title}.md)\n')
            title_list.append(title)

        
    for i, c in enumerate(collection_list):
        title = c['post']['title']
        print(title)
        title = title.replace('/', '_')

        # 如果文件已存在，则跳过
        if os.path.exists(f'{collection_path}/{i+1}-{title}.md'):
            continue

        # 保存文章内容
        with open(f'{collection_path}/{i+1}-{title}.md', 'w', encoding='utf-8') as t:
            t.write(f'## {title}\n')
            content = c['post']['content']

            # 去除多余标签
            content = content.replace('</p>', '')
            content = content.replace('　　', '')
            content = content.replace('&nbsp;', '')
            content = content.replace('<br /> ', '')
            pattern = re.compile(r'<p id=".*"  >')
            content = re.sub(pattern, '', content)

            t.write(content)

            if i > 0:
                t.write(f'上一篇： [{title_list[i-1]}](./{title_list[i-1]}.md)\n\n')
            if i < len(title_list) - 1:
                t.write(f'下一篇： [{title_list[i+1]}](./{title_list[i+1]}.md)\n\n')



if __name__ == '__main__':
    # 保存路径
    save_path = './results'

    # 合集ID，可根据APP端的分享链接获取
    collection_id = 20460170

    # 保存合集
    save_collection(collection_id, save_path)
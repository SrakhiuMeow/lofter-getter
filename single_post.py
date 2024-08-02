from utils.get_by_api import get_post
import json
import os

if __name__ == '__main__':
    
    save_path = './results/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    blog_id = 0
    post_id = 0
    
    posts = get_post(blog_id, post_id)['posts']
    for i in posts:
        print(i['post']['title'])
        with open(f'{save_path}{i["post"]["title"].replace("/", "_")}.html', 'w', encoding='utf-8') as f:
            f.write(i['post']['content'])
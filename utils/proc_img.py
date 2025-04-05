import re
import requests
import os

def replace_img_url(content, title=None, cvt2local=False, rename=True):
    # 替换图片URL
    pattern = re.compile(r'<img src=".*?".*')
    label_list = re.findall(pattern, content)
    img_url_list = [label.split('="', 1)[1].split('?')[0] for label in label_list]
    img_name_list = []

    # TODO: 还要考虑标题重复的可能
    for i, img in enumerate(img_url_list):
        if cvt2local:
            if rename:
                img_name = f'{title}_{i}.jpg' if i > 0 else f'{title}.jpg'
            else:
                img_name = img.split('/')[-1]
            img_name_list.append(img_name)
            content = content.replace(label_list[i], f'![img](images/{img_name})')
        else:
            img_name = img.split('/')[-1]
            img_name_list.append(img_name)
            content = content.replace(label_list[i], f'![img]({img})')
    return content, img_url_list, img_name_list


def download_img(img_url_list, img_name_list, save_path):
    # 下载图片
    for i, img in enumerate(img_url_list):
        # img_name = img.split('/')[-1]
        img_name = img_name_list[i]
        # img_name = img_name.split('?')[0]
        img_path = f'{save_path}/{img_name}'
        # 如果文件存在，则增加后缀
        # TODO: 可能会有文件名冲突的问题
        if os.path.exists(img_path):
            img_path = f'{save_path}/{img_name.split(".")[0]}_{i}.jpg'

        # TODO: 需要多线程
        with open(img_path, 'wb') as f:
            f.write(requests.get(img.split('?')[0]).content)


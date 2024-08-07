import re
import requests

def replace_img_url(content, cvt2local=False):
    # 替换图片URL
    pattern = re.compile(r'<img src=".*?".*')
    label_list = re.findall(pattern, content)
    img_list = [label.split('="', 1)[1].split('?')[0] for label in label_list]

    for i, img in enumerate(img_list):
        if cvt2local:
            img_name = img.split('/')[-1]
            content = content.replace(label_list[i], f'![img](images/{img_name})')
        else:
            content = content.replace(label_list[i], f'![img]({img})')
    return content, img_list


def download_img(img_list, save_path):
    # 下载图片
    for i, img in enumerate(img_list):
        img_name = img.split('/')[-1]
        # img_name = img_name.split('?')[0]
        img_path = f'{save_path}/{img_name}'

        with open(img_path, 'wb') as f:
            f.write(requests.get(img.split('?')[0]).content)


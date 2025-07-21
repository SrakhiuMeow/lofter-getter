import re
import requests
import os
from concurrent.futures import ThreadPoolExecutor

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


def download_img(img_url_list, img_name_list, save_path, max_workers=5):
    # 下载图片


        def download_single_image(img_url, img_name, save_path, index):
            for i, img in enumerate(img_url_list):
                # img_name = img.split('/')[-1]
                img_name = img_name_list[i]
                # img_name = img_name.split('?')[0]
                img_path = f'{save_path}/{img_name}'
                # 如果文件存在，则增加后缀
                # TODO: 可能会有文件名冲突的问题
                if os.path.exists(img_path):
                    img_path = f'{save_path}/{img_name.split(".")[0]}_{i}.jpg'

                clean_url = img_url.split('?')[0]

                try:
                    response = requests.get(clean_url, stream=True)
                    response.raise_for_status()
                    with open(img_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    return True
                except Exception as e:
                    print(f"Failed to download {img_url}: {str(e)}")
                    return False
                
        os.makedirs(save_path, exist_ok=True)
    

        # 多线程
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Prepare arguments for each download task
            tasks = [
                (url, name, save_path, i) 
                for i, (url, name) in enumerate(zip(img_url_list, img_name_list))
            ]
            
            # Submit all tasks and wait for completion
            results = list(executor.map(
                lambda args: download_single_image(*args), 
                tasks
            ))
        return results


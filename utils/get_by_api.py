import json

import requests

try:
    import brotli
except ImportError:
    print('请先安装brotli，运行"pip install brotli"即可')
    exit(1)

def get_subs(authkey, offset=0, limit_once=50):
    # 获取订阅列表，需要登录信息(LOFTER-PHONE-LOGIN-AUTH) 
    url = "https://api.lofter.com/newapi/subscribeCollection/list.json"
    params = {
    'offset': offset,
    'limit': limit_once
    }

    headers = {
    'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
    'Accept-Encoding': "br,gzip",
    'lofter-phone-login-auth': authkey,
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


def get_post(blog_id, post_id):
    # 获取文章详情
    url = "https://api.lofter.com/oldapi/post/detail.api"

    params = {
    'product': "lofter-android-7.6.12"
    }

    payload = f"targetblogid={blog_id}&supportposttypes=1%2C2%2C3%2C4%2C5%2C6&offset=0&requestType=1&postdigestnew=1&postid={post_id}&blogId={blog_id}&checkpwd=1&needgetpoststat=1"

    headers = {
    'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
    'Accept-Encoding': "br,gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'lofproduct': "lofter-android-7.6.12",
    }

    response = requests.post(url, params=params, data=payload, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)['response']
    else:
        return None
    

def get_collection_list(collection_id, offset, limit=15, authkey=None, order=1):
    # 获取合集详情，包括列表
    # order为返回顺序
    url = "https://api.lofter.com/v1.1/postCollection.api"

    params = {
    'product': "lofter-android-7.6.12"
    }

    # payload = f"method=getCollectionDetail&offset={offset}&limit={limit}&collectionid={collection_id}&blogid={blog_id}&order={order}"
    payload = f"method=getCollectionDetail&offset={offset}&limit={limit}&collectionid={collection_id}&order={order}"

    headers = {
    'Accept-Encoding': "br,gzip",
    'content-type': "application/x-www-form-urlencoded; charset=utf-8",
    }

    if authkey is not None:
        headers['lofter-phone-login-auth'] = authkey

    response = requests.post(url, params=params, data=payload, headers=headers)

    return json.loads(response.text)['response']

def get_collections_by_author(author_id,offset=0, limit=15, authkey=None,order=1):
    #获取一个作者的所有合集信息
    #order为返回顺序
    url="https://api.lofter.com/v1.1/postCollection.api?product=lofter-android-8.0.18"
    blog_domain=author_id+".lofter.com"
    file_path="utils\cookie.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        cookie_str = f.read().strip()

    headers = {
        "Host": "api.lofter.com",
          "Cookie": cookie_str
    }

    data = {
    "blogdomain": blog_domain,
    "method": "getCollectionList",
    "needViewCount": "1",
}
    response = requests.post(url, headers=headers,data=data, verify=False)

    try:
        return json.loads(response.text)['response']
    except KeyError:
        return None



def get_collection(blog_domain, collection_id, blog_id, authkey=None):
    # 获取合集信息
    url = "https://api.lofter.com/v1.1/postCollection.api"

    params = {
    'product': "lofter-android-7.6.12"
    }

    payload = f"blogdomain={blog_domain}&method=getCollection&collectionid={collection_id}&blogid={blog_id}"

    headers = {
    'Accept-Encoding': "br,gzip",
    'content-type': "application/x-www-form-urlencoded; charset=utf-8",
    }

    if authkey is not None:
        headers['lofter-phone-login-auth'] = authkey

    response = requests.post(url, params=params, data=payload, headers=headers)
    # import ipdb
    # ipdb.set_trace()
    return json.loads(response.text)['response']

def get_user_info(user_id, authkey):
    # 获取用户信息
    url = "https://api.lofter.com/newapi/user/info.json"

    params = {
    'userId': user_id
    }

    headers = {
    'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
    'Accept-Encoding': "br,gzip",
    'lofter-phone-login-auth': authkey,
    }

    response = requests.get(url, params=params, headers=headers)

    return json.loads(response.text)['response']

def get_my_info(authkey):
    # 获取我的信息
    url = "https://api.lofter.com/v1.1/usercounts.api"

    params = {
        'product': "lofter-android-7.6.12"
    }

    headers = {
        'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
        'Accept-Encoding': "br,gzip",
        'lofter-phone-login-auth': authkey,
    }

    response = requests.get(url, params=params, headers=headers)

    return json.loads(response.text)['response']


def get_history(authkey, blogdomain, offset=0, limit=50):
    # 获取历史记录
    url = "https://api.lofter.com/v2.0/history.api"

    params = {
        'method': 'getList',
        'offset': offset,
        'limit': limit,
        'blogdomain': blogdomain,
        'product': 'lofter-android-7.6.12'
    }

    headers = {
        'lofproduct': 'lofter-android-7.6.12',
        'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
        'Accept-Encoding': "br,gzip",
        'lofter-phone-login-auth': authkey,
    }

    response = requests.get(url, params=params, headers=headers)

    return json.loads(response.text)['response']


def get_page_comments(blog_id, post_id, offset=0, limit=10, authkey=None):
    # 获取所有评论
    url = "https://api.lofter.com/comment/l1/page.json"

    params = {
        'postId': post_id,
        'blogId': blog_id,
        'offset': offset,
        'limit': limit # 该参数无效
    }

    headers = {
        'lofproduct': 'lofter-android-7.6.12',
        'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
        'Accept-Encoding': "br,gzip",
    }

    if authkey is not None:
        headers['lofter-phone-login-auth'] = authkey

    response = requests.get(url, params=params, headers=headers)

    if json.loads(response.text)['code'] == 0:
        return json.loads(response.text)['data']
    else:
        raise Exception('获取评论失败')
    

def get_l2_comments(blog_id, post_id, id, offset):
    # 获取子评论
    ...
    


def get_comments_by_pid(blog_id, post_id, pid, offset=0, limit=50):
    # 获取划线评论
    url = "https://api.lofter.com/comment/pCommentList.json"

    params = {
        'postId': post_id,
        'blogId': blog_id,
        'pid': pid,
        'offset': offset,
        'limit': limit
    }

    headers = {
        'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
        'Accept-Encoding': "br,gzip",
        
    }

    

    response = requests.get(url, params=params, headers=headers)

    return json.loads(response.text)['data']



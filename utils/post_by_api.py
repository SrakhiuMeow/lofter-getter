import requests

def post_like(authkey, post_id, blog_id, dislike=False):
    # 点赞，不能用
    url = "https://api.lofter.com/v1.1/like.api"

    params = {
        'product': "lofter-android-7.6.12"
    }
    headers = {
        'User-Agent': "LOFTER-Android 7.6.12 (V2272A; Android 13; null) WIFI",
        'lofter-phone-login-auth': authkey,
        'content-type': "application/x-www-form-urlencoded; charset=utf-8",
        'Accept-Encoding': "br,gzip",
    }

    body = {
        'scene': 'note',
        'blogid': blog_id,
        'postid': post_id
    }

    if dislike:
        body['liketype'] = 'unlike'

    response = requests.post(url, params=params, headers=headers, data=body)
    print(response.text)
    return response.text
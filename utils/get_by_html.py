import requests

def get_post(url, authkey):
    # 通过Lofter网页端获取文章详情，需要登录
    url = url.replace('http://', 'https://')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Encoding': "br,gzip",
        'lofter-phone-login-auth': authkey,
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    with open('post.html', 'w', encoding='utf-8') as f:
        f.write(response.text)


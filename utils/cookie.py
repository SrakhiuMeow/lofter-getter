try:
    import browser_cookie3 as browsercookie
except ImportError:
    print('请先安装browser_cookie3，运行"pip install browser_cookie3"即可')
    exit(1)
import requests

def get_lofter_authkey(browser='default'):
    # 通过获取浏览器的cookie得到登录信息(LOFTER-PHONE-LOGIN-AUTH)
    # 浏览器需要已经登录lofter
    
    if browser == 'default':
        cookie = browsercookie.load()
    else:
        try:
            cookie = getattr(browsercookie, browser)()
        except:
            raise ValueError('browser should be one of "chrome", "firefox", "edge", "opera", "opera_gx", '+
                             '"librewold", "chromium", "brave", "vivaldi, "safari", "w3m", "lynx", "default"')
    

    cookie = requests.utils.dict_from_cookiejar(cookie)
    try:
        authkey = cookie['LOFTER-PHONE-LOGIN-AUTH']
    except:
        authkey = None
        print('请在浏览器中登录lofter后再重试')
        exit(1)
    
    return authkey

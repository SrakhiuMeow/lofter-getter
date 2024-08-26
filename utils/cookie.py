import browser_cookie3 as browsercookie
import requests

def get_lofter_authkey(browser='default'):
    # 通过获取浏览器的cookie得到登录信息(LOFTER-PHONE-LOGIN-AUTH)
    # 浏览器需要已经登录lofter
    
    
    if browser == 'chrome':
        cookie = browsercookie.chrome()            
    elif browser == 'firefox':
        cookie = browsercookie.firefox()
    elif browser == 'default':
        cookie = browsercookie.load()
    else:
        raise ValueError('browser should be one of "chrome", "firefox", "default"')
        
    cookie = requests.utils.dict_from_cookiejar(cookie)
    try:
        authkey = cookie['LOFTER-PHONE-LOGIN-AUTH']
    except:
        authkey = None
    
    return authkey

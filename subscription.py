import argparse
from utils.cookie import get_lofter_authkey
from utils.save_content import save_subs


# 保存路径
save_path = './results'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save history from lofter')

    parser.add_argument('--save_path', type=str, default=save_path, help='Save path')
    parser.add_argument('--save_img', action='store_true', help='Save images')
    parser.add_argument('--limit_once', type=int, default=50, help='Limit of fetching once')
    parser.add_argument('--browser', type=str, default='default')
    parser.add_argument('--authkey', type=str, default='', help='LOFTER-PHONE-LOGIN-AUTH')
    args = parser.parse_args()

    # 需要登录信息(LOFTER-PHONE-LOGIN-AUTH)
    # 可自行填写或者自动获取（需要浏览器已经登陆lofter）
    if args.authkey:
        authkey = args.authkey
    else:
        authkey = get_lofter_authkey(browser=args.browser)
    # authkey = 'your_authkey_here' # 手动填写   

    save_subs(authkey, args.save_path, sleep_time=0.1, limit_once=args.limit_once)
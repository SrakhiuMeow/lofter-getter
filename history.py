import argparse
from utils.cookie import get_lofter_authkey
from utils.save_content import save_history
from utils.get_by_api import get_my_info

save_path = './results'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save history from lofter')

    parser.add_argument('--save_path', type=str, default=save_path, help='Save path')
    parser.add_argument('--save_img', action='store_true', help='Save images')
    parser.add_argument('--limit_once', type=int, default=50, help='Limit of fetching once')
    parser.add_argument('--browser', type=str, help='default')
    args = parser.parse_args()

    authkey = get_lofter_authkey(browser=args.browser)




    my_info = get_my_info(authkey)
    home_page_url = my_info['blogs'][0]['blogInfo']['homePageUrl'][8:]

    save_history(authkey, home_page_url, save_path, save_img=args.save_img, limit_once=args.limit_once)
from utils.cookie import get_lofter_authkey
from utils.save_content import save_history
from utils.get_by_api import get_user_info

save_path = './results'

authkey = get_lofter_authkey(browser='default')


save_history(authkey, '你的博客地址', save_path)
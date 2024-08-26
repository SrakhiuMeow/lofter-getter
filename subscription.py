from utils.cookie import get_lofter_authkey
from utils.save_content import save_subs


# 保存路径
save_path = './results'

# 需要登录信息(LOFTER-PHONE-LOGIN-AUTH)
# 可自行填写或者自动获取（需要浏览器已经登陆lofter）
authkey = get_lofter_authkey(browser='default')  # 自动获取
# authkey = 'your_authkey_here' # 手动填写

save_subs(authkey, save_path, sleep_time=0.1)
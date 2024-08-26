from utils.save_content import save_single_collection

# 保存路径
save_path = './results'

# 合集ID，可根据APP端的分享链接获取
collection_id = 21297998

# 保存合集
save_single_collection(collection_id, save_path, save_img=False, rewrite=False)
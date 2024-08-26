from utils.save_content import save_single_post


# 保存路径
save_path = './results'

# 博客ID和文章ID，可根据APP端的分享链接获取
blog_id = 0
post_id = 0

save_single_post(blog_id, post_id)

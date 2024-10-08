from utils.save_content import save_single_post
import argparse


# 保存路径
save_path = './results'

# 博客ID和文章ID，可根据APP端的分享链接获取
blog_id = 0
post_id = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save single post from lofter')
    
    parser.add_argument('blog_id', type=int, default=blog_id, help='Blog ID')
    parser.add_argument('post_id', type=int, default=post_id, help='Post ID')
    parser.add_argument('--save_path', type=str, default=save_path, help='Save path')
    parser.add_argument('--rewrite', action='store_true', help='Rewrite existing files')

    args = parser.parse_args()

    # 保存文章
    save_single_post(args.blog_id, args.post_id, args.save_path, rewrite=args.rewrite)
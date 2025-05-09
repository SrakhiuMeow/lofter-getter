import argparse
import json

from utils.save_content import save_single_collection
from utils.get_by_api import get_collections_by_author


# 保存路径
save_path = './results'

# 必须修改cookie值文件才能使用！请看readme文档


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save Collections by An Author. It requires your Cookie!!!')

    parser.add_argument('--author_id', type=str, default=None ,help='author_id, NOT user_name!')
    parser.add_argument('--save_path', type=str, default=save_path, help='Save path')
    parser.add_argument('--save_img', action='store_true', help='Save images')
    parser.add_argument('--rewrite', action='store_true', help='Rewrite existing files')
    parser.add_argument('--limit_once', type=int, default=50, help='Limit of fetching once')
    parser.add_argument('--epub', action='store_true', help='Generate epub')
    parser.add_argument('--pdf', action='store_true', help='Generate pdf')

    args = parser.parse_args()
    author= args.author_id
    
    collections=get_collections_by_author(author)['collections']
    ids=[]
    for collection in collections:
        ids.append(collection['id'])

    # 保存合集
    for id in ids:
        save_single_collection(int(id), args.save_path, save_img=args.save_img, rewrite=args.rewrite,
                           limit_once=args.limit_once, create_epub=args.epub, create_pdf=args.pdf)



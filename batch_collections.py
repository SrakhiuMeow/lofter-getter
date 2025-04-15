from utils.save_content import save_single_collection
import argparse

# 保存路径
save_path = './results'

# 合集ID，可根据APP端的分享链接获取


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch saving multiple collections by ids')

    parser.add_argument('--collection_ids', type=str, default=None ,help='Collection IDs')
    parser.add_argument('--save_path', type=str, default=save_path, help='Save path')
    parser.add_argument('--save_img', action='store_true', help='Save images')
    parser.add_argument('--rewrite', action='store_true', help='Rewrite existing files')
    parser.add_argument('--limit_once', type=int, default=50, help='Limit of fetching once')
    parser.add_argument('--epub', action='store_true', help='Generate epub')
    parser.add_argument('--pdf', action='store_true', help='Generate pdf')

    args = parser.parse_args()
    ids = args.collection_ids.split(',')

    # 保存合集
    for id in ids:
        save_single_collection(int(id), args.save_path, save_img=args.save_img, rewrite=args.rewrite,
                           limit_once=args.limit_once, create_epub=args.epub, create_pdf=args.pdf)

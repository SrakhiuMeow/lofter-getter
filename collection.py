from utils.save_content import save_single_collection
import argparse

# 保存路径
save_path = './results'

# 合集ID，可根据APP端的分享链接获取
collection_id = 20194917

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save single collection from lofter')
    
    parser.add_argument('collection_id', type=int, default=collection_id ,help='Collection ID')
    parser.add_argument('--save_path', type=str, default=save_path, help='Save path')
    parser.add_argument('--save_img', action='store_true', help='Save images')
    parser.add_argument('--rewrite', action='store_true', help='Rewrite existing files')

    args = parser.parse_args()

    # 保存合集
    save_single_collection(args.collection_id, args.save_path, save_img=args.save_img, rewrite=args.rewrite)

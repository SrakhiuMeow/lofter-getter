## 项目介绍
利用Lofter API获取合集(Collection)信息，并爬取其内容，保存下来。  
（支持文字内容和图片，为了方便查看将原本的HTML内容转换为Markdown格式，但是转换暂时不够完全）  

API是通过对Lofter Android客户端进行抓包分析得到的，随时可能失效  

根据合集ID(collectionId)获取合集列表  
遍历下载合集内每篇文章的内容

代码水平很烂，凑合一下（  
有问题可以提Issue，也许会解决（

## 使用须知
在Lofter APP中分享合集，选择复制链接，则可以得到对应的合集ID

也可以使用subscrption.py，获取浏览器已登录的lofter账号的合集订阅列表，来批量获得合集ID

请合理使用该脚本，不得滥用

**使用之前需要安装依赖**
```bash
pip install -r requirements.txt
```
否则会报错



## 程序文件说明
#### collection.py
根据合集ID批量下载合集内容  
更改最后部分的collection_id即可更改要下载的合集  
save_img参数决定是否将图片保存都本地  
rewrite参数决定是否替换本地已存在的合集文件

#### subscrption.py
根据从浏览器获取的登录信息获得订阅合集的信息  
暂时没有进一步处理数据的功能，现在可以用来获取当前订阅的合集ID


## 常见问题
```
  File "get_by_api.py", line 72, in get_collection_list
    return json.loads(response.text)['response']
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "save_content.py", line 41, in save_single_collection
    collection = get_collection_list(collection_id,  0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "collection.py", line 10, in <module>
    save_single_collection(collection_id, save_path, save_img=False, rewrite=False)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```
 
需要安装brotli  
`pip install brotli`  
或者在程序根目录下执行  
`pip install -r requirements.txt`  
安装所有依赖库
## 项目介绍
利用Lofter API获取合集(Collection)信息，并爬取其内容，保存下来。  

API是通过对Lofter Android客户端进行抓包分析得到的，随时可能失效  

根据合集ID(collectionId)获取合集列表  
遍历下载合集内每篇文章的内容

代码水平很烂，凑合一下（  
有问题可以提Issue，也许会解决（

## 注意
在Lofter APP中分享合集，选择复制链接，则可以得到对应的合集ID与博客ID  
部分需要登录的操作应当传入authkey，即从浏览器获得的lofter-phone-login-auth  
需要安装brotli，否则会报错

## 安装环境
```bash
pip install -r requirements.txt
```
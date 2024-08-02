## 项目介绍
利用Lofter API获取合集(Collection)信息，并爬取其内容，保存下来。
也许可以提供一个前端界面来查看合集内容

API是通过对Lofter Android客户端进行抓包分析得到的，随时可能实效

根据合集ID(collectionId)获取合集列表
遍历下载合集内每篇文章的内容

## 注意
部分需要登录的操作应当传入authkey，即从浏览器获得的lofter-phone-login-auth
# 根据豆瓣分类标签爬取豆瓣图书

2020年11月 爬取图书数据8万条和相关图书评论若干，并存储图书图片

## 1. 配置

### 代理配置
蘑菇代理隧道代理  
Notice: 由于ip质量问题，有时会返回状态码200，但是重定向显示 "Your IP is restricted" 所以在middleware中处理  

## 2. 使用
1. 配置python环境 `pip install -r requirements.txt`
2. 根据settings格式，设置mysql和redis
3. 开启爬虫 `python -m run`

# ScrapyDemo
Pytnon2.7 + Scrapy 测试项目

## 使用说明
```sh
pip install scrapy

cd ScrapyDemo

# 爬 http://www.kuaidaili.com 的代理并存入数据库
scrapy crawl KuaiDaiLiSpider

# 爬 http://www.xicidaili.com 的代理并存入数据库
scrapy crawl XiCiDaiLiSpider
```

## TODO
* [ ] 使用代理并自动随机切换、自动筛选无效代理
      * IP池项目: https://github.com/qiyeboy/IPProxyPool
* [ ] 多线程
* [x] 自动换 User-Agent
* [ ] 表单登录处理、Cookies
* [ ] 爬图片、文件的测试

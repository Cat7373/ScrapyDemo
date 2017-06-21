# ScrapyDemo
Pytnon2.7 + Scrapy 测试项目

## 使用说明
```sh
cd ScrapyDemo

# 爬 http://www.kuaidaili.com 的代理并存入数据库
scrapy crawl KuaiDaiLiSpider

# 爬 http://www.xicidaili.com 的代理并存入数据库
scrapy crawl XiCiDaiLiSpider
```

## TODO
* [ ] 使用代理并自动随机切换、自动筛选无效代理
* [ ] 多线程
* [x] 自动换 User-Agent
* [ ] 表单登录处理、Cookies
* [ ] 来源检查处理(Referer)
* [ ] 根据响应头中的编码或 meta(html文件) 中的编码来设置相应的编码

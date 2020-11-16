import json
import re
from urllib import parse
import scrapy
from scrapy.loader import ItemLoader
from scrapy import Request
import requests

from articleSpider.items import JobBoleArticleItem, ArticleItemLoader
from utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        # esponse.xpath()
        # extract_first()
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")
        # url = response.css('#news_list h2.news_entry a::attr(href)').extract_first("")
        # url = response.xpath('//*[@id="entry_675219"]/div[2]/h2/a/@href').extract_first("")
        # 原生 Selector(text=response.text).css() |.xpath()
        # 抓取图片url 和详情地址
        # 获取子节点
        post_node = response.css('#news_list .news_block')
        for node in post_node:
            pic_url = node.css('.entry_summary a img::attr(src)').extract_first("")
            if pic_url.startswith('//'):
               pic_url = 'https:'+pic_url
            detail_url = node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, detail_url),meta={'front_img_url': pic_url},callback=self.parse_detail)

        # 提取下一页 并交给parse下载
        # next = response.css('.pager a:last-child::text').extract_first("")
        next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first()
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        # if(next == 'Next >'):
        #     next_url = response.css('.pager a:last-child::attr(href)').extract_first("")
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

    def parse_detail(self, response):
        #实例item
        # article_item = JobBoleArticleItem()
        # #获取详情页的内容 id title  content poster post_time tags comment_count  view_count recommend_count
        # reg = re.match(".*?(\d+)",response.url)
        # if reg:
        #     id =reg.group(1)
        #     title = response.css('#news_title a::text').extract_first("")
        #     poster = response.css('#news_info .news_poster a::text').extract_first("")
        #     post_time = response.css('#news_info .time::text').extract_first("")
        #     #提取出日期
        #     reg_time = re.match(".*?(\d+.*)", post_time)
        #     if reg_time:
        #         post_time = reg_time.group(1)
        #     content = response.css('#news_content').extract()[0]  # 富文本格式
        #     tags_list = response.css('.news_tags a::text').extract()  # list 类型 需要处理
        #     tags = ",".join(tags_list)
        #     article_item['title'] = title
        #     article_item['content'] = content
        #     article_item['url'] = response.url
        #     article_item['image_origin_path'] = [response.meta.get("front_img_url", "")]
        #     article_item['post_time'] = post_time
        #     article_item['tags'] = tags
        #     article_item['poster'] = poster
        reg = re.match(".*?(\d+)", response.url)
        id = reg.group(1)
        # 通过 itemLoader改写上面的代码
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", "#news_title a::text")
        item_loader.add_css('poster', '#news_info .news_poster a::text')
        item_loader.add_css('post_time', '#news_info .time::text')
        item_loader.add_css('content', '#news_content')
        item_loader.add_css('tags', '.news_tags a::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('image_origin_path', response.meta.get("front_img_url", ""))


        #发送请求 取别的xhr数据 https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId=676059
        yield Request(url=parse.urljoin(response.url,"/NewsAjax/GetAjaxNewsInfo?contentId={}".format(id)),meta={'article_item':item_loader,'url':response.url},callback=self.parse_nums)


        pass
    def parse_nums(self, response):
        arr = json.loads(response.text)
        # article_item = response.meta.get('article_item', '')
        # comment_count = arr['CommentCount']
        # view_count = arr['TotalView']
        # recommend_count = arr['DiggCount']
        # article_item['comment_count'] = comment_count
        # article_item['view_count'] = view_count
        # article_item['recommend_count'] = recommend_count
        # article_item['url_md5_id'] = get_md5(article_item['url'])
        item_loader = response.meta.get('article_item', '')
        item_loader.add_value('comment_count', arr['CommentCount'])
        item_loader.add_value('view_count', arr['TotalView'])
        item_loader.add_value('recommend_count', arr['DiggCount'])
        item_loader.add_value('url_md5_id', get_md5(response.meta.get('url')))
        article_item = item_loader.load_item()
        yield article_item



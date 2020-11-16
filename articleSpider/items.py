# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
# 测试
def addTitle(value):
    return value+'-------------'+'ithua'
# 日期转换
def dateFormate(value):
    reg_time = re.match(".*?(\d+.*)", value)
    if reg_time:
       return reg_time.group(1)
    else:
        return '1970-1-1'


# 自定义ArticleItemLoader
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    #id title  content poster post_time tags comment_count  view_count recommend_count
    title = scrapy.Field(
      # input_processor = MapCompose(addTitle),
      #  output_processor =TakeFirst()
    )
    content = scrapy.Field()
    url = scrapy.Field()
    url_md5_id = scrapy.Field()
    image_origin_path = scrapy.Field( # 必须是字典所以必须单独设置
        output_processor=Identity()
    )
    image_save_path = scrapy.Field()
    post_time = scrapy.Field(
        input_processor=MapCompose(dateFormate)
    )
    tags = scrapy.Field(
        output_processor=Join(separator=",")
    )
    poster = scrapy.Field()
    comment_count = scrapy.Field()
    view_count = scrapy.Field()
    recommend_count = scrapy.Field()


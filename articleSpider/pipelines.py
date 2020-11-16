# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json

import MySQLdb
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item



#获取图片地址
class ArticleImagesPipeline(ImagesPipeline):
    #重写方法
    def item_completed(self, results, item, info):
        if 'image_origin_path' in item:
            for ok, value in results:
                image_file_path = value['path']
            item['image_save_path'] = image_file_path
        return item


#将item写入文件
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('item.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


#第二种方式
class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('item2.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

#将数据插入数据库
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'spider_article', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO `jobbole` (`url_md5_id`, `title`, `content`, ` url`, ` image_origin_path`, ` image_save_path`, 
            `poster`, `comment_count`, `view_count`, `recommend_count`, `tags`, `post_time`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE comment_count=VALUES(comment_count)

        """
        params = list()
        params.append(item.get('url_md5_id', ''))
        params.append(item.get('title', ''))
        params.append(item.get('content', ''))
        params.append(item.get('url', ''))
        params.append(item.get('image_origin_path', ''))
        image_save_path = ','.join(item.get('image_save_path', []))
        params.append(image_save_path)
        params.append(item.get('poster', ''))
        params.append(item.get('comment_count', ''))
        params.append(item.get('view_count', ''))
        params.append(item.get('recommend_count', ''))
        params.append(item.get('tags', ''))
        params.append(item.get('post_time', ''))
        self.cursor.execute(insert_sql, tuple(params))
        self.conn.commit()
        return item

#异步插入数据库（推荐）
class MysqlTwisterPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, setting):
        from MySQLdb.cursors import DictCursor
        dbparams = dict(
            host=setting['MYSQL_HOST'],
            db=setting["MYSQL_DBNAME"],
            user=setting['MYSQL_USER'],
            passwd=setting['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    #处理错误
    def handle_error(self, failure, item, spider):
        print(failure)

    #执行插入
    def do_insert(self, cursor,  item):
        insert_sql = """
                 INSERT INTO `jobbole` (`url_md5_id`, `title`, `content`, ` url`, ` image_origin_path`, ` image_save_path`, 
                 `poster`, `comment_count`, `view_count`, `recommend_count`, `tags`, `post_time`) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE comment_count=VALUES(comment_count)

             """
        params = list()
        params.append(item.get('url_md5_id', ''))
        params.append(item.get('title', ''))
        params.append(item.get('content', ''))
        params.append(item.get('url', ''))
        params.append(item.get('image_origin_path', ''))
        # image_save_path = item.get('image_save_path', [])
        params.append(item.get('image_save_path', []))
        params.append(item.get('poster', ''))
        params.append(item.get('comment_count', ''))
        params.append(item.get('view_count', ''))
        params.append(item.get('recommend_count', ''))
        params.append(item.get('tags', ''))
        params.append(item.get('post_time', ''))
        cursor.execute(insert_sql, tuple(params))

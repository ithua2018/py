from scrapy.cmdline import execute
import sys
import os
# 添加执行环境的路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 执行需要的脚本名称
# execute(["scrapy","crawl","jobbole"])

execute(["scrapy", "crawl", "zhihu"])
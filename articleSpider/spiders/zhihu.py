import pickle
import time
import scrapy
from mouse import click, move
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        pass



    def start_requests(self):

        from selenium.webdriver.chrome.options import Options
       #  chrom_option = Options()
       #  chrom_option.add_argument("--disable-extensions")
       #  chrom_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
       #  browser = webdriver.Chrome(executable_path="D:/chromedriver_win32/chromedriver.exe", chrome_options=chrom_option)
       # #  browser.get('https://www.zhihu.com/signin')
       #  browser.get('https://www.zhihu.com/')
       #  browser.find_elements_by_css_selector(".SignFlow-tab")[1].click()
       #  # browser.find_element_by_css_selector('.SignFlow-accountInput input').send_keys(Keys.CONTROL+"a")
       #  browser.find_element_by_css_selector('.SignFlow-accountInput input').send_keys('673509045@qq.com')
       #  # browser.find_element_by_css_selector('.SignFlow-password input').send_keys(Keys.CONTROL+"a")
       #  browser.find_element_by_css_selector('.SignFlow-password input').send_keys('112956hua')
       #  time.sleep(3)
       #  move(680, 480)
       #  click()
       # # browser.find_element_by_css_selector('.Button.SignFlow-submitButton').click()
       #  time.sleep(60)
       # 将cookie保存到文件中
       #  cookies = browser.get_cookies()
       #  pickle.dump(cookies, open('D:/vitrualenvhome/articleSpider/cookies/zhihu.cookies', 'wb'))
       # 从文件读取cookie
        cookies = pickle.load(open('D:/vitrualenvhome/articleSpider/cookies/zhihu.cookies', 'rb'))
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]




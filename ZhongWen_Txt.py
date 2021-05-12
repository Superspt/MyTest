import requests
import re

demo = 'https://www.qzguermei.com'

class MySpider:

    def __init__(self):
        self.session = requests.Session() # 下载器

    # 爬取页面html信息
    def MyPage(self, myurl, encoding='utf-8'):
        res = self.session.get(myurl)
        res.encoding = encoding
        return res.text

    # 爬取每个页面的链接信息
    def MyChapter(self, html):
        body_ul = re.findall(r'<h2>全职艺术家 章节目录</h2>.*?</ul>', html, re.S)[0]
        info = re.findall(
            r'<li><a href="(.*?)" title=".*?" target="_blank">(.*?)</a></li>',
            "".join(body_ul))
        return info

    # 爬取页面内容
    def MyContent(self, chpt_url):
        chpt_html = self.MyPage(chpt_url, encoding='utf-8')
        pattern = re.compile(
            r'<div class="content" id="chaptercontent">(.*?)</div>',
            re.S)
        chpt_content = re.findall(pattern, chpt_html)
        chpt_content = "".join(chpt_content)
        # 数据处理
        chpt_content = chpt_content.replace('\n', '')
        chpt_content = chpt_content.replace(' ', '')
        # \u3000表示中文中的全角空格
        chpt_content = chpt_content.replace('\u3000', '')
        chpt_content = chpt_content.replace('<br/>', '')
        chpt_content = chpt_content.replace('全书网手机阅读地址https://m.qzguermei.com', '')
        return chpt_content

    # 对页面循环下载，自动下载得到所有文档
    def MyText(self, url):
        html = self.MyPage(url, encoding='utf-8')
        chpter_urls = self.MyChapter(html)
        i = 1
        for url in chpter_urls:
            # 创建一个文件 小说章节名.txt
            fb = open('Article_C/Article_%d_C.txt' % i, 'w', encoding="utf-8")
            i = i + 1
            # 下载内容
            content = self.MyContent(demo + url[0])
            # 这个chapter_info[0]是指一个数据里的第一个信息，也就是链接
            fb.write(content)
            fb.close()

if __name__=='__main__':
    url ='https://www.qzguermei.com/d/2169/'
    mySpider = MySpider()
    mySpider.MyText(url)
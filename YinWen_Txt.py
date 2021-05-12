import requests
import re  # 内库

demo = 'http://en.people.cn'

class MySpider:
    def __init__(self, num):
        self.session = requests.Session()
        # 这个n用来标记页面编号
        self.n = num

    # 循环下载得到所有内容
    def MyText(self, url):
        # 得到整个页面的信息
        index_html = self.MyPage(url, encoding='utf-8')
        # 得到每个要爬取的页面的信息，并存在变量chpter_urls中
        chpter_urls = self.MyContent(index_html)
        # 循环下载每个链接中的页面信息
        for url in chpter_urls:
            fb = open('Article_E/Article_%d_E.txt' % self.n, 'w', encoding="utf-8")
            # 下载内容，只需要url中第一个位置的信息即可
            content = self.MyContent(demo + url[0])
            self.n += 1
            fb.write(content)
            fb.close()

    # 爬取整个页面的html信息
    def MyPage(self, url, encoding="utf-8"):
        res = self.session.get(url)
        res.encoding = encoding
        return res.text

    # 获取每个章节的链接
    def MyChapter(self, index_html):
        links = re.findall(
            r'<div class="on1 clear"><h3><a href=\'(.*?)\' target=_blank>(.*?)</a></h3></div>',
                           index_html, re.S)
        return links

    # 下载每个章节的内容
    def MyContent(self, chapter_url):
        chapter_html = self.MyPage(chapter_url, encoding='utf-8')
        content = \
            re.findall(
                r'<div class="w860 d2txtCon cf">.*?</div>(.*?)<div class="share_text cf">',
                chapter_html, re.S)[0]
        content = "".join(content)
        # 数据清洗
        content = content.replace('\r\n', '')
        content = content.replace('&quot;', '')
        content = content.replace('<h1>', '')
        content = content.replace('</h1>', '')
        content = content.replace('<p>', '')
        content = content.replace('</p>', '')
        pattern = re.compile(r'<div class="origin cf">.*?</div>')
        content = re.sub(pattern, "", content)  # 排除链接
        pattern2 = re.compile(r'<div class="editor">.*?</div>')
        content = re.sub(pattern2, "", content)  # 排除作者
        pattern3 = re.compile(r'\n{2,}')
        content = re.sub(pattern3, '\n', content)  # 排除作者
        pattern4 = re.compile(r'(\n\t{1,}){2,}')
        content = re.sub(pattern4, '\n\t', content)  # 排除作者
        content = content.replace('</div>', '')
        return content


if __name__ == '__main__':
    novel_url = 'http://en.people.cn/90782/index'
    novel_url1 = 'http://en.people.cn/business/index'
    novel_url2 = 'http://en.people.cn/90882/index'
    n = 1
    spider = MySpider(n)  # 实例化
    for i in range(1, 20):
        spider.MyText(novel_url + str(i) + '.html')
    for j in range(1, 20):
        spider.MyText(novel_url1 + str(j) + '.html')
    for j in range(1, 20):
        spider.MyText(novel_url2 + str(j) + '.html')

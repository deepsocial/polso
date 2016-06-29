from AmisScraper.items import NewsArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime


class BloombergSpider(CrawlSpider):
    name = "bloomberg"
    logf = open("bloomberg.log", "w")
    allowed_domains = ["bloomberg.com"]
    start_urls = ["http://www.bloomberg.com"]
    rules = [
        Rule(LinkExtractor(allow='(/news/articles/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        try:
            item['title'] = title
            item['article'] = article
            item['link'] = response.url
            raw_date = response.url.split("/")[-2]
            date = datetime.strptime(raw_date, '%Y-%m-%d')
            item['date'] = str(date)
            return item
        except Exception as e:
            self.logf.write("Failed to scrape {0}: {1}\n".format(str(title), str(e)))


class NoggersBlogSpider(CrawlSpider):
    name = "noggers"
    logf = open("noggers.log", "w")
    allowed_domains = ["nogger-noggersblog.blogspot.it"]
    start_urls = ["http://nogger-noggersblog.blogspot.it/"]
    rules = [
        Rule(LinkExtractor(allow='((?!:).)*html$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//a/text()')[8].extract()
        article = response.xpath('//div/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        try:
            token = filter(lambda x: '--' in x, article)
            try:
                raw_date = token[0].split(' -- ')[0].replace('\n', '')
                date = datetime.strptime(raw_date, '%d/%M/%y')
            except (ValueError, IndexError):
                try:
                    raw_date = title.split("Nogger's Blog: ")[1]
                    date = datetime.strptime(raw_date, '%d-%b-%Y')
                except (ValueError, IndexError):
                    date = ""
            item['date'] = str(date)
            return item
        except Exception as e:
            self.logf.write("Failed to scrape {0}: {1}\n".format(str(title), str(e)))


class WorldGrainSpider(CrawlSpider):
    name = "worldgrain"
    logf = open("worldgrain.log", "w")
    allowed_domains = ["world-grain.com"]
    start_urls = ["http://www.world-grain.com"]
    rules = [
        Rule(LinkExtractor(allow='(/articles/news_home/)((?!:).)*$'), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow='(/news_home/)((?!:).)*$'), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow='(/articles/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        try:
            raw_date = "{0}-{1}".format(response.url.split("/")[-2], response.url.split("/")[-3])
            date = datetime.strptime(raw_date, '%m-%Y')
            item['date'] = str(date)
            return item
        except Exception as e:
            self.logf.write("Failed to scrape {0}: {1}\n".format(str(title), str(e)))


class EuractivSpider(CrawlSpider):
    name = "euractiv"
    logf = open("euractiv.log", "w")
    allowed_domains = ["www.euractiv.com"]
    start_urls = ["http://www.euractiv.com"]
    rules = [
        Rule(LinkExtractor(allow='(/agriculture-food/news/)((?!:).)*$'), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow='(/news/)((?!:).)*$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        article = response.xpath('//p/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title
        item['article'] = article
        item['link'] = response.url
        try:
            raw_date = article[3].replace(" ", "").replace("\n", "").replace("\t", "")
            date = datetime.strptime(raw_date, '%d/%m/%Y')
            item['date'] = str(date)
            return item
        except Exception as e:
            self.logf.write("Failed to scrape {0}: {1}\n".format(str("title"), str(e)))


class AgriMoneySpider(CrawlSpider):
    name = "agrimoney"
    logf = open("agrimoney.log", "w")
    allowed_domains = ["www.agrimoney.com"]
    start_urls = ["http://www.agrimoney.com", "http://www.agrimoney.com/search/news/"]
    rules = [
        Rule(LinkExtractor(allow='(/news/)((?!:).)*html$$'), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow='(/feature/)((?!:).)*html$$'), callback="parse_item", follow=True),
        Rule(LinkExtractor(allow='(/marketreport/)((?!:).)*html$$'), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        item = NewsArticleItem()
        title = response.xpath('//title/text()')[0].extract()
        raw_date = response.xpath('//font/text()')[2].extract().split(',')[1] + \
                   response.xpath('//font/text()')[3].extract().split(',')[0]
        article = response.xpath('//p/text()').extract() + response.xpath('//p/font/text()').extract()
        self.logger.info("Scraping Title: "+title)
        item['title'] = title.replace('Agrimoney.com | ', '')
        item['article'] = article
        item['link'] = response.url
        try:
            date = datetime.strptime(raw_date.split(',')[1], ' %d %b %Y')
            item['date'] = str(date)
            return item
        except (ValueError, IndexError):
            raw_date = response.xpath('//font/text()')[2].extract() + response.xpath('//font/text()')[3].extract()
            try:
                date = datetime.strptime(raw_date.split(',')[2], ' %d %b %Y')
                item['date'] = str(date)
                return item
            except (ValueError, IndexError):
                try:
                    date = datetime.strptime(raw_date.split(',')[1], ' %d %b %Y')
                    item['date'] = str(date)
                    return item
                except Exception as e:
                    self.logf.write("Failed to scrape {0}: {1}\n".format(str(title), str(e)))

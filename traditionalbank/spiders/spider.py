import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import TtraditionalbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class TtraditionalbankSpider(scrapy.Spider):
	name = 'traditionalbank'
	start_urls = ['https://www.traditionalbank.com/about-us/bank-news?page=0']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Go to next page"]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		date = response.xpath('//p[@class="date"]/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//article[@class="content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=TtraditionalbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()

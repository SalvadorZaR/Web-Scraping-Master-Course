from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Video(Item):
    titulo = Field()
    descripcion = Field()
    fecha = Field()

class Reseñas(Item):
    titulo = Field()
    descripcion = Field()
    fecha = Field()

class Noticias(Item):
    titulo = Field()
    descripcion = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT':50
    }

    allowed_domains = ['latam.ign.com']
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps5&order_by=']
    
    download_delay = 1

    

    rules = (
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True), # HORIZONTALIDAD POR TIPO => No tiene callback ya que aqui no voy a extraer datos
        Rule(LinkExtractor(
            allow=r'&page=\d+'
            ), follow=True), # HORIZONTALIDAD DE PAGINACION EN CADA TIPO => No tiene callback ya que aqui no voy a extraer datos
        
        # Una regla por cada tipo de contenido donde ire verticalmente
        # Cada una tiene su propia funcion parse que extraera los items dependiendo de la estructura del HTML donde esta cada tipo de item
        Rule(
            LinkExtractor( # VERTICALIDAD DE REVIEWS
                allow=r'/review/'
            ), follow=True, callback='parse_review'),
        Rule(
            LinkExtractor( # VERTICALIDAD DE VIDEOS
                allow=r'/video/'
            ), follow=True, callback='parse_video'),
        Rule(
            LinkExtractor(
                allow=r'/news/' # VERTICALIDAD DE ARTICULOS
            ), follow=True, callback='parse_news'),
    )


    def parse_video(self,response):
        item = ItemLoader(Video(),response)
        item.add_xpath('titulo','//h1[@id="id_title"]/text()')
        item.add_xpath('descripcion','//div[@id="id_deck"]/text()')
        item.add_xpath('fecha','//span[@class="publish-date"]/text()')

        yield item.load_item()
    
    
    def parse_reseñas(self,response):
        item = ItemLoader(Reseñas(),response)
        item.add_xpath('titulo','//div[@class="article-headline"]/h1/text()')
        item.add_xpath('descripcion','//div[@class="article-sub-headline"]/h3/text()')
        item.add_xpath('fecha','//div[@class="article-publish-date"]/span/text()')

        yield item.load_item()

    def parse_noticias(self,response):
        item = ItemLoader(Noticias(), response)
        item.add_xpath('titulo','//h1[@id="id_title"]/text()')
        item.add_xpath('descripcion','//div[@class="article-sub-headline"]/h3/text()')

        yield item.load_item()
                          
    






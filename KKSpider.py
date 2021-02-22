import re
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Join, MapCompose
# for scope in response.xpath('//div[@itemscope]'):
#     print("current scope:", scope.xpath('@itemtype').getall())
#     props = scope.xpath('''
#                 set:difference(./descendant::*/@itemprop,
#                                .//*[@itemscope]/*/@itemprop)''')
#     print(f"    properties: {props.getall()}")
def clean_desc(values):
    return values.strip()
def clean_discount(values):
    return values.strip()
def clean_img(images):
    base = "https://www.knifekits.com/vcom/"
    tmp=images.split(',')
    images=[base + t.strip() for t in tmp]
    return images
def fix_price_json(data):
    results = []
    for i,price in enumerate(data):
        tmp = [PRICE.replace('$','') for PRICE in price]
        results.append(tmp)
    return results
def fix_images_json(data):
    base_url = "https://knifekits.com/vcom/images/"
    for i, img in enumerate(data):
        tmp = [IMG.replace('images/','') for IMG in img.split(',')]
        results.append({str(i):tmp})
    return results

def fix_images_forreal(data):
    p = re.compile(r"'.+\.jpg'")
    for item in data:
        images = item.all_images.split("'")[1::2]
    return images

class KKItem(scrapy.Item):
    sku = scrapy.Field()
    all_images = scrapy.Field(
        output_processor=MapCompose(clean_img))
    
    cannonical_url = scrapy.Field()
    video_url = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field(
        output_processor=MapCompose(clean_desc)
    )
    test_description = scrapy.Field(
    )
    price = scrapy.Field(MapCompose(fix_price))

    discount_tiers = scrapy.Field(
        input_processor=MapCompose(clean_discount),
        output_processor=Join()
    )
    discount_amount = scrapy.Field(
        input_processor=MapCompose(clean_discount),
        output_processor=Join()
    )
    keywords = scrapy.Field()
    link = scrapy.Field()
    products_id = scrapy.Field()

class KnifekitsSpider(scrapy.Spider):
    name = "knifekits"
    start_urls = [
        # "https://www.knifekits.com/vcom/knife-making-kitsblades-c-1070.html"
        # "https://www.knifekits.com/vcom/knife-making-handles-c-40.html"

        # "https://www.knifekits.com/vcom/holster-making-materials-boltaron-c-1071_500.html",
        # "https://www.knifekits.com/vcom/holster-making-materials-holstex-c-1071_430.html",
        # "https://www.knifekits.com/vcom/holster-making-materials-kydex-c-1071_54.html",
        "https://www.knifekits.com/vcom/holster-making-materials-leather-c-1071_264.html",
        # "https://www.knifekits.com/vcom/holster-making-materials-thermoform-sheet-swatch-c-1071_544.html",
        
    ]
    pattern = re.compile("https://.+.html",re.DOTALL)

    def parse(self, response):
        pattern = re.compile("https://.+.html",re.DOTALL)
        links = response.xpath('//div[@class="col-sm-4"]/descendant::a/@href').re(pattern)
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_category)
    
    def parse_category(self, response):
        pattern = re.compile("https://.+.html",re.DOTALL)
        category_links = response.xpath('//div[@class="productHolder equal-height"]/a/@href').re(pattern)
        for link in category_links:
            yield scrapy.Request(url=link, callback=self.parse_detail)
    
    def parse_detail(self, response):
        pattern = re.compile("https://.+.html",re.DOTALL)
        product_loader = ItemLoader(item=KKItem(), response=response)
        product_loader.default_output_processor = TakeFirst()
        
        description = [d.strip() for d in response.xpath('//div[@itemprop="description"]/p/descendant-or-self::text()').getall()]

        product_loader.add_xpath(
            'sku',
            './/span[@itemprop="model"]/descendant-or-self::text()'
        )
        product_loader.add_xpath(
            'all_images',
            './/*[@class="thumbnail"]/@data-image',
        )
        product_loader.add_xpath(
            'sku',
            './/*[@class="thumbnail"]/@data-caption'
        )
        product_loader.add_xpath(
            'cannonical_url',
            '//link[@rel="canonical"]/@href'
        )
        product_loader.add_xpath(
            'video_url',
            './/link[@rel="canonical"]/@href'
        )
        product_loader.add_xpath(
            'name',
            './/h1/descendant::span[@itemprop="name"]/text()'
        )
        product_loader.add_xpath(
            'title',
            '/html/head/title/text()'
        )
        product_loader.add_xpath('price', './/*[@itemprop="price"]/text()'.replace('$',''),)
        
        product_loader.add_xpath(
            'discount_tiers',
            './/*[@class="DiscountPriceQty"]/text()'
        )
        product_loader.add_xpath(
            'discount_amount',
            './/*[@class="DiscountPrice"]/text()',
        )
        product_loader.add_xpath(
            'keywords',
            './/meta[@name="keywords"]/@content',

        )
        product_loader.add_value(
            'link',
            response.url
        )
        product_loader.add_xpath(
            'products_id',
            '//input[@name="products_id"]/@value'
        )
        product_loader.add_value(
            'description', description
        )
        yield product_loader.load_item()
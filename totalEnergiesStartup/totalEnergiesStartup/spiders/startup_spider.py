import scrapy


class StartupsSpider(scrapy.Spider):
    name = "startups"
    start_urls = [
        'https://startupper.totalenergies.com/fr/juries/4Q26wmPMC7he1rxgPoOIUA/participations/6735/vote?order=random',
 ]


    def parse(self, response):
        for startup in response.css('div.super-card'):
            yield {
                'captain': startup.css('p.text-secondary a::text').get(),
                'name': startup.css('div.over-hidden h5.font-weight-medium::text').get(),
                'description': startup.css('div.content-sm p.m-b-none::text').get(),
            }
            
        next_page = response.css('div.media-left a.right-project::attr(href)').get()
        previous_page = response.css('div.media-left a.left-project::attr(href)').get()
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
        if previous_page is not None:
            previous_page = response.urljoin(previous_page)
            yield scrapy.Request(previous_page, callback=self.parse)
        
        

import scrapy

class NuforcSpyder(scrapy.Spider):
    '''
    A spyder for report index by month on nuforc.org website
    '''

    name = "nuforc"
    start_urls = ['http://www.nuforc.org/webreports/ndxevent.html']

    def parse(self, response):
        '''
        Parses index page with links to monthly reports
        '''
        for link in response.xpath('//table//tr//td//a/@href').extract():
            yield response.follow(link, self.parse_table)

    def parse_table(self, response):
        '''
        Parses monthly report page
        '''
        for row in response.xpath('//table//tbody//tr'):
            fields = row.xpath('td')
            yield {
                'date_time': fields[0].xpath('font//a/text()').extract_first(),
                'city': fields[1].xpath('font/text()').extract_first(),
                'state': fields[2].xpath('font/text()').extract_first(),
                'shape': fields[3].xpath('font/text()').extract_first(),
                'duration': fields[4].xpath('font/text()').extract_first(),
                'summary': fields[5].xpath('font/text()').extract_first(),
                'posted': fields[6].xpath('font/text()').extract_first(),
            }

# -*- coding: utf-8 -*-
import scrapy
from great_schools.items import GreatSchoolsItem

class GreatschoolsSpider(scrapy.Spider):
    name = "great_schools"
    allowed_domains = ["greatschools.org"]
    start_urls = ['https://www.greatschools.org/new-york/new-york/schools/' + s for s in [''] + ['?page=' + str(i) for i in range(2,3)]]

    def parse(self, response):

        schools = response.xpath('//div[@class="pvm gs-bootstrap js-schoolSearchResult js-schoolSearchResultCompareErrorMessage"]')
        
        for school in schools:
            
            name = school.xpath('.//a/text()').extract_first()
            gs_rating_overall = school.xpath('.//div[@class="row"]//a/span[starts-with(@class, "gs-rating")]/text()').extract_first()
            review_count = school.xpath('.//div[@class="row"]//a[@class="font-size-small js-reviewCount"]/text()').extract_first()
            school_type = school.xpath('.//div[@class="row"]//div[@class="prs fl"]/text()').extract_first()
            grades_served = school.xpath('.//div[@class="row"]//div[@class="fl"][2]/text()').extract_first()
            link = 'https://www.greatschools.org' + school.xpath('.//a/@href').extract_first()

            
            yield scrapy.Request(link, callback=self.parse_each, meta={'name': name,
                                                                    'gs_rating_overall': gs_rating_overall,
                                                                    'review_count': review_count,
                                                                    'school_type': school_type,
                                                                    'grades_served': grades_served})

    def parse_each(self, response):
        
        name = response.meta['name']
        gs_rating_overall = response.meta['gs_rating_overall']
        review_count = response.meta['review_count']
        school_type = response.meta['school_type']
        grades_served = response.meta['grades_served']
        info = response.xpath('/html/head/script[@type="application/ld+json"][2]/text()').extract()

        item = GreatSchoolsItem()

        item['name'] = name
        item['gs_rating_overall'] = gs_rating_overall
        item['review_count'] = review_count
        item['school_type'] = school_type
        item['grades_served'] = grades_served
        item['info'] = info


        academics = response.xpath('//div[@id="academics-tour-anchor"]//div[contains(@class, "toc-entry")]')
        tests = response.xpath('//div[@id="TestScores"]//div[starts-with(@class,"test-score-container")]')
        
        gs_rating_academics = []

        for academic in academics:
            indicator = academic.xpath('./a/span[not(@*)]/text()').extract_first()
            rating = academic.xpath('./a/span[contains(@class, "gs-rating")]/text()').extract_first()
            
            if indicator is not None:
                if rating is None:
                    rating = ''
                try:
                    gs_rating_academics.append(indicator.strip() + ':' + rating.strip())
                except:
                    continue
            
        gs_rating_academics = ';'.join(gs_rating_academics)
        

        test_scores = []

        for test in tests:
            subject = test.xpath('./div[contains(@class,"subject") and text()!="Subject" and not(*)]/text() | ./div[contains(@class,"subject")]/span/text()').extract_first()
            proficiency_perc = test.xpath('.//div[@class="score" and not(*)]/text() | .//div[@class="score"]/span/text()           ').extract_first()
            state_avg = test.xpath('.//div[@class="state-average"]/text()').extract_first()

            if subject is not None:
                if proficiency_perc is None:
                    proficiency_perc = ''
                if state_avg is None:
                    state_avg=''
                
                try:
                    test_scores.append(subject.strip() + ':' + proficiency_perc.strip() + ':' + state_avg.strip()[11:])
                except:
                    continue

        
        test_scores = ';'.join(test_scores)

        item['gs_rating_academics'] = gs_rating_academics
        item['test_scores'] = test_scores


        yield item

		
		
import scrapy
import os

# Add else-part that checks using command line arguments


rem_urls_file = 'links.txt'

auth_file = 'auth.txt'

n_courses = 6

class LoginSpider(scrapy.Spider):
    name = 'moodle'
    start_urls=['https://moodle.iitb.ac.in/login/index.php']
    # def start_requests(self):
    #     if (os.path.exists(auth_file) and os.path.exists(rem_urls_file)):
    #         i = 10
    #         with open(rem_urls_file, 'rb') as urls:
    #             for url in urls:
    #                 yield scrapy.Request(url, self.parse, priority=i)
    #                 i -= 1
       
    def parse(self, response):
        #print("Expecting username followed by password on next line...")
        auth = open(auth_file, 'r')
        username = auth.readline().split("\n", 1)[0]
        password = auth.readline().split("\n", 1)[0]
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': username, 'password': password},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        else:
            course_hrefs = []
            for course in response.css('h3.coursename')[:n_courses] :
                course_name = course.xpath('a/text()').extract_first()
                course_hrefs.append(course.css('a::attr(href)').extract_first())
            for course_href in course_hrefs :
                yield response.follow(course_href, callback=self.parse_course)

    def parse_course(self, response):
        page_title = response.css('div.page-header-headings')

        ann_dict = dict()

        for ele in page_title :
            course_name = page_title.css('h1::text').extract_first()
            announcements = response.css('div.activityinstance')
            ann_href = []
            for announcement in announcements :
                # [1:] since first is a link to forum
                ann_href.append(announcement.css('a::attr(href)').extract_first())
            ann_dict[course_name] = ann_href
        return ann_dict
    

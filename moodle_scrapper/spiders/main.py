import scrapy
import os

# Add else-part that checks using command line arguments


rem_urls_file = 'links.txt'

auth_file = 'auth.txt'

n_courses = 7

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
        print("Expecting username followed by password on next line...")
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
            for course in response.css('h3.coursename')[:n_courses] :
                course_name = course.css('a::attr(href)').extract_first()
                print course_name
                

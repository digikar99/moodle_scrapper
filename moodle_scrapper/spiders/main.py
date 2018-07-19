import scrapy
import getpass
import json

inputArr = raw_input().split()
href_name = dict()

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
        #auth = open(auth_file, 'r')
        username=inputArr[0]
        #print username
        password=inputArr[1]
        #username = auth.readline().split("\n", 1)[0]
        #password = auth.readline().split("\n", 1)[0]
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': username, 'password': password},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            print "Authentication failed!"
            self.logger.error("Login failed")
            return
        else:
            n_courses = inputArr[2]
            course_names = []
            name_href = dict()
            #print "Number of courses: ", n_courses
            for course in response.css('h3.coursename')[: int(n_courses)] :
                course_name = course.xpath('a/text()').extract_first()
                course_href = course.css('a::attr(href)').extract_first()
                course_names.append(course_name)
                name_href[course_name] = course_href
            if inputArr[3] == "yes" :
                # if running for the first time, save links
                with open("links.json", 'w') as links_file :
                    json.dump(name_href,links_file)
            global href_name
            for course_name in course_names :
                href_name[name_href[course_name]] = course_name
                yield response.follow(name_href[course_name], callback=self.parse_course)

    def parse_course(self, response):
        page_title = response.css('div.page-header-headings')
        course_href = response.request.url
       
        ann_dict = dict()

        for ele in page_title :
            #course_name = page_title.css('h1::text').extract_first()
            full_name = href_name[course_href]
            announcements = response.css('div.activityinstance')
            ann_dict[full_name] = []
            for announcement in announcements[1:] :
                # [1:] since first is a link to forum
                null = None
                ann_dict[full_name].append(announcement.css('span.instancename::text').extract_first())
                ann_dict[full_name].append(announcement.css('a::text').extract_first())
                try:
                    ann_dict[full_name].remove(null)
                except:
                    pass
                

            #ann_dict[course_name] = ann_href
        return ann_dict
    

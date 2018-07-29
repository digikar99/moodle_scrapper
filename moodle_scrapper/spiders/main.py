import scrapy
import getpass
import json

inputArr = raw_input().split()
href_name = dict()
ann_name = dict()
upd_dict = dict()

# These dicts are used for storage of links and page names;
# as scrapy works asynchronously. This means that there is no
# way to tell of which course the returned page 'response'
# belongs. The exact course names are important, since they
# are used to notify the users which course pages have been changed.

## 1. The process starts with the parse function.
##    It tries to authenticate. Its result is sent to after_login
##    function.
## 2. after_login function checks if authentication was successful.
##    If successful, then it checks if the spider has been run for the
##    first time - whether or not course names and href pairs have
##    been saved in a file.
## 3. If not ran for the first time, it simply proceeds to open
##    each of the course_href. Its response is sent to the parse_course
##    function

class LoginSpider(scrapy.Spider):
    name = 'moodle'
    start_urls=['https://moodle.iitb.ac.in/login/index.php']
       
    def parse(self, response):
        username=inputArr[0]
        password=inputArr[1]
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': username, 'password': password},
            callback=self.after_login
        )

    def after_login(self, response):
        # check whether login succeeded before going on
        if "authentication failed" in response.body:
            print "Authentication failed!"
            self.logger.error("Login failed")
            return
        else:
            n_courses = inputArr[2]
            course_names = []
            name_href = dict()
            for course in response.css('h3.coursename')\
                [: int(n_courses)]:
                course_name = course.xpath('a/text()').extract_first()
                course_href = course.css('a::attr(href)')\
                                    .extract_first()
                course_names.append(course_name)
                name_href[course_name] = course_href
            if inputArr[3] == "yes" :
                # if running for the first time, save links
                with open("links.json", 'w') as links_file :
                    json.dump(name_href,links_file)
            global href_name
            for course_name in course_names :
                href_name[name_href[course_name]] = course_name
                yield response.follow(name_href[course_name],\
                                      callback=self.parse_course)

    def parse_course(self, response):
        #page_title = response.css('div.page-header-headings')
        course_href = response.request.url
       
        global upd_dict

        #for ele in page_title :
        #course_name = page_title.css('h1::text').extract_first()
        full_name = href_name[course_href]
        updates = response.css('div.activityinstance')
        upd_dict[full_name] = []

        # The first link is that of 'Announcements'
        for update in updates[1:] :
            null = None
            upd_dict[full_name].append(update\
                                       .css('span.instancename::text')\
                                       .extract_first())
            upd_dict[full_name].append(update.css('a::text')\
                                       .extract_first())
            try:
                upd_dict[full_name].remove(null)
            except:
                pass

        #print "=========== OLD Upd_dict: ========", upd_dict

        announcement=updates[0].css('a::attr(href)').extract_first()
        ann_name[announcement] = full_name

        #print "========== ANNOUNCEMENT ===========", announcement
        yield response.follow(announcement, callback=self.parse_ann)

        #print "============ NEW upd_dict: ========", upd_dict    
       
            
        #return upd_dict

    def parse_ann(self, response):
        #print "\n ============= PARSE_ANN is called ================"
        #print "\n======== Topics: ======\n", response.css('td.topic starter')
        topics=response.css('td.starter')
        full_name = ann_name[response.request.url]
        global upd_dict
        for topic in topics:
            upd_dict[full_name].append(topic.css('a::text').extract_first())

        #print "========= NEW DICT ========= ", upd_dict
#       
#        return upd_dict

    def close(self, reason):
        print "============= Close called ==========="
        with open("updates.json", 'a') as updates_file :
            json.dump(upd_dict, updates_file)

        
    

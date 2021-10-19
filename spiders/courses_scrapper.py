import scrapy
from udsmtimetable_scrapper.items import TimetableItem

class CoursesScrapperSpider(scrapy.Spider):
    name = 'courses_scrapper'
    allowed_domains = ['https://timetable.udsm.ac.tz/resource/g12501.html#parent']
    start_urls = ['https://timetable.udsm.ac.tz/resource/g12501.html#parent']

    # def parse(self, response):
    #     for li in response.css("ul")[0].css("li"):
    #         name = li.css("a::text").get()
    #         url = li.css("a").attrib["href"]
    #         course = CoursesItem(name=name, code = name)
    #         yield course

    def parse(self, response):
        count = 0
        for tr in response.css("table").css("tr"):

            if 0 <= count <= 108:
                day = "Monday"
            elif 108 < count <= 216:
                day = "Tuesday"
            elif 216 < count <= 326:
                day = "Wednesday"
            elif 326 < count <= 439:
                day = "Thursday"
            elif 439 < count <= 546:
                day = "Friday"
            else:
                day = None
            
            for td in tr.css("td"):
                # print("\n\n\n\n "+ td.get() +" \n\n\n\n")
                try:
                    t_ = td.css("a::text")[1:].get()
                    
                    type_ = t_.split(", ")[0] 
                    time = t_.split(", ")[1] 
                    fro = time.split("-")[0]
                    to = time.split("-")[1]

                    all_remain = td.css("a")[1:]
                    
                    rooms = []
                    for a in all_remain:
                        if a.css("a").attrib["href"][0] == 'r':
                            rooms.append(a.css('a::text').get())
                    
                    groups = []
                    for a in all_remain:
                        if a.css("a").attrib["href"][0] == 'g':
                            groups.append(a.css('a::text').get())
                    
                    for group in groups:
                        for room in rooms:
                            timetable = TimetableItem(type_=type_, fro=fro, to=to, rooms=room, courses=group, day=day)
                            yield timetable
                    else:
                        pass

                except:
                    continue

            count += 1




# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import psycopg2
import requests as rq
from settings import API_URL

# base_url = "http://127.0.0.1:8000/"
base_url = API_URL

token_url = base_url+"api-token-auth/"
course_url = base_url+"courses/"
room_url = base_url+"rooms/"
period_url = base_url+"periods/"

s_course_url = base_url+"search_course/"
s_room_url = base_url+"search_room/"
s_period_url = base_url+"search_period/"
clear_periods_url = base_url+"clear_periods/"

class UdsmtimetableScrapperPipeline:

    header = {}
    cleared = False
    
    def open_spider(self, spider):
        token = rq.post(base_url+"api-token-auth/", {'username':'admin','password':'changeme'}).json()["token"]
        self.header = {'Authorization': "Token "+token} 
        ms = rq.get(clear_periods_url, headers=self.header).json()["message"]
        if ms == "clear":
            self.cleared = True

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        
        if self.cleared:
            try:
                course = rq.post(course_url, {"code":item["courses"]}, headers=self.header).json()["course"]
                
            except:
                course = rq.post(s_course_url, {"code":item["courses"]}, headers=self.header).json()["course"]

            try:
                room = rq.post(room_url, {"name":item["rooms"]}, headers=self.header).json()["room"]
            except:
                room = rq.post(s_room_url, {"name":item["rooms"]}, headers=self.header).json()["room"]

            period = rq.post(period_url, {"type":item["type_"], "day":item['day'], "room":room["url"], "course":course["url"], "from_time":item["fro"], "to_time":item["to"]}, headers=self.header).json()
            
            return period

        pass



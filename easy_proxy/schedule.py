from time import sleep
from .setting import spyder_list,HOST,IP,DB,db_list

from .base_classes.proxy_route import start_run
from threading import Thread
from .base_classes.proxy_check import validUsefulProxy



class CheckThread(Thread):
    def __init__(self,threadID, name, counter):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("start check")
        check_method()

class CrawlThread(Thread):
    def __init__(self,threadID, name, counter):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("start crawl")
        crawl_thread()

class RouteThread(Thread):
    def __init__(self,threadID, name, counter):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("start route")
        route_method()

def crawl_thread():
    db = db_list[DB]
    while True:
        for li in spyder_list:
            db.append(li.crawl())
        sleep(60)

def route_method():
    db = db_list[DB]
    start_run(IP,HOST,db)

def check_method():
    db = db_list[DB]
    while True:
        host = db.choice_waitting()
        if host is None:
            sleep(20)
        else:
            if validUsefulProxy(host):
                print("valid host {}".format(host))
                db.append_check(host)
            else:
                print("valid faild {}".format(host))

        # host = db.choice()
        # if host is None:
        #     pass
        # else:
        #     if not validUsefulProxy(host):
        #         print("valid faild {} in checked, remove it.".format(host))
        #         db.remove(host)


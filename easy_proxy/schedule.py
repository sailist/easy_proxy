from time import sleep
from .setting import spyder_list,HOST,IP,db

from .base_classes.proxy_route import start_run
from threading import Thread
from .base_classes.proxy_check import validUsefulProxy



class CheckThread(Thread):
    def __init__(self,threadID, name, counter,db):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.db = db
        self.counter = counter

    def run(self):
        print("start check")
        check_method(self.db)

class CrawlThread(Thread):
    def __init__(self,threadID, name, counter,db):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.db = db
    def run(self):
        print("start crawl")
        crawl_thread(self.db)

class RouteThread(Thread):
    def __init__(self,threadID, name, counter,db):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.db = db
    def run(self):
        print("start route")
        route_method(self.db)

def crawl_thread(db):
    while True:
        for li in spyder_list:
            db.append(li.crawl())
        sleep(60)

def route_method(db):
    start_run(IP,HOST,db)

def check_method(db):
    while True:
        host = db.choice_waitting()
        if host is None:
            sleep(20)
        else:
            if validUsefulProxy(host):
                db.append_check(host)
            else:
                print("valid faild {}".format(host))

        sleep(10)
        host = db.choice()
        if host is None:
            sleep(20)
        else:
            if not validUsefulProxy(host):
                print("valid faild {}".format(host))
                db.remove(host)


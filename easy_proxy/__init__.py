
from .base_classes import *
from .proxyes import *
from .databases import *
from .schedule import CrawlThread,RouteThread,CheckThread
from threading import Thread
from .setting import THREAD_NUM,ONLY_STORE,DB,db_list

def run():
    db = db_list[DB]()

    thread_list = []
    thread_list.append(CrawlThread(1,"crawl",1,db))

    if not ONLY_STORE:
        thread_list.append(RouteThread(2,"route",2,db))

    for i in range(THREAD_NUM["check"]):
        ch = CheckThread(i,"check_{}".format(i),i,db)
        thread_list.append(ch)

    for ch in thread_list:
        ch.start()

    for ch in thread_list:
        ch.join()
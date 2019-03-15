import random
import json
import os

class Proxy_Simple_Db():
    store_path = "{}/{}".format(os.path.split(__file__)[0],"proxy.json")

    def __init__(self):
        print("initial simple db file...")
        if os.path.exists(self.store_path):
            with open(self.store_path) as f:
                self.wait_valid = json.load(f)

        else:
            self.proxys = {}
            with open(self.store_path,"w") as w:
                json.dump(self.proxys,w)

        self.proxys = {}
        print("initial over.")



    def append(self,host):
        '''
        通过key-value的形式添加进去，保证不会重复
        :param host:
        :return:
        '''
        if type(host) == list:
            for i in host:
                self.wait_valid[i] = 1
        elif type(host) == str:
            self.wait_valid[host] = 1

    def append_check(self,host):
        if type(host) == list:
            for i in host:
                print("valid host:{}".format(i))
                self.proxys[i] = 1
        elif type(host) == str:
            self.proxys[host] = 1
            print("valid host:{}".format(host))

        self.save()

    def choice(self):
        if len(self.proxys) == 0:
            return None
        return random.choice(list(self.proxys))

    def choice_waitting(self):
        if len(self.wait_valid) == 0:
            return None
        return self.wait_valid.popitem()[0]

    def getall_waitting(self):
        return self.wait_valid.keys()

    def getall(self):
        return self.proxys.keys()

    def remove(self,host):
        if hasattr(self.proxys,host):
            self.proxys.pop(host)
            self.save()

    def clear(self):
        self.proxys.clear()

    def save(self):
        with open(self.store_path,"w") as w:
            json.dump(self.proxys,w)


db = Proxy_Simple_Db()
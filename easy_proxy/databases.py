from .base_classes.proxy_store import BaseDB
import json
import os
import redis
import random
from .setting import db_list
from functools import wraps

def database_class(cls):
    db_list[cls.__name__] = cls()


@database_class
class Proxy_Simple_Db(BaseDB):
    def __init__(self):
        self.store_path = "{}/{}".format(os.path.split(__file__)[0], "proxy.json")
        print("initial simple db file...")
        if os.path.exists(self.store_path):
            with open(self.store_path) as f:
                self.wait_valid = json.load(f)
        else:
            self.proxys = {}
            self.wait_valid = {}
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
                self.proxys[i] = 1
        elif type(host) == str:
            self.proxys[host] = 1
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

@database_class
class RedisDB(BaseDB):
    '''
    proxy:valid:{sorted set}
    proxy:uncheck:{set}

    '''
    def __init__(self,**kw):
        import redis
        print("initial redis db...")
        self.valid_key = "proxy:valid"
        self.uncheck_key = "proxy:uncheck"

        self.pool = redis.ConnectionPool(db = 1)
        self.db = redis.Redis(connection_pool= self.pool)
        self.db.flushdb()
        if self.db.exists(self.valid_key):
            hold = self.db.zrevrange(self.valid_key,0,-1)
            for h in hold:
                self.db.sadd(self.uncheck_key,h)
            self.db.zremrangebyrank(self.valid_key,0,-1)
        print("initial over.")

    def append(self, host):
        if type(host) == list:
            for h in host:
                self.db.sadd(self.uncheck_key, h)
        elif type(host) == str:
            self.db.sadd(self.uncheck_key, host)

    def append_check(self, host):
        if type(host) == list:
            for h in host:
                self.db.zadd(self.valid_key, {h:1})
        elif type(host) == str:
            self.db.zadd(self.valid_key, {host:1})

    def choice(self):
        result = self.db.zrevrange(self.valid_key,0,-1)
        if len(result) == 0:
            return None
        return random.choice(result).decode()

    def choice_waitting(self):
        result = self.db.spop(self.uncheck_key,1)
        if len(result) == 0:
            return None
        return result[0].decode()

    def getall_waitting(self):
        sets = self.db.smembers(self.uncheck_key)
        sets = [s.decode() for s in sets]
        return sets

    def getall(self):
        sets = self.db.zrevrange(self.valid_key,0,-1)
        sets = [s.decode() for s in sets]
        return sets

    def remove(self, host):
        self.db.zrem(self.valid_key,host)

    def clear(self):
        # self.db.
        pass

    def save(self):
        self.db.save()


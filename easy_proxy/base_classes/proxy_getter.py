from lxml import etree
import re
from easy_proxy.base_classes.requests import WebRequest


_re_proxy_format = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}")
_request = WebRequest()
class BaseProxy:
    def __init__(self, url_list = [], func_list = [], before_callback = [], after_callback = [],err = "warning"):
        self.url_list = url_list
        self.func_list = func_list
        self.before_req_func = before_callback
        self.after_req_func = after_callback
        self.err_type = err
        pass
    def _base_callback(self,url,func_list):
        if func_list is None:
            return url
        for func in func_list:
            url = func(url)
        return url
    def before_request(self,url,func_list):
        return self._base_callback(url,func_list)

    def after_request(self, response, func_list):
        return self._base_callback(response, func_list)

    def _validate(self):
        if not hasattr(self,"before_req_func"):
            self.before_req_func = []
        if not hasattr(self,"after_req_func"):
            self.after_req_func = []
        if not hasattr(self,"err_type"):
            self.err_type = "warning"

    def _check_host(self,p):
        if not re.search(_re_proxy_format, p):
            if self.err_type == "warning":
                print("'{}' is not a ip format ,please check your func_list".format(p))
            return False
        return True
    def crawl(self):
        '''
        获取一个list
        :return:
        '''
        self._validate()

        final = []
        for url in self.url_list:
            url = self.before_request(url,self.before_req_func)
            response = _request.get(url)
            response = self.after_request(response,self.after_req_func)
            for func in self.func_list:
                response = func(response)
            final += response## 确保到这一步已经是全ip:port的形式的list了

        final = [p for p in final if self._check_host(p)]
        print("crawl {} of host in {}".format(len(final),str(self.__class__)))
        return final

    def __str__(self):
        return "base_proxy"

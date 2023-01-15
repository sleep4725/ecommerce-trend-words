from urllib.parse import urlencode
'''
11번가
'''
class ModelOfHmall:
    
    def __init__(self) -> None:
        self._flag :str= "hmall"
        self._url :str= "https://www.hmall.com/p/bma/getPopScwd.do"
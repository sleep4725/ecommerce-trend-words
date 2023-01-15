from urllib.parse import urlencode
'''
홈플러스
'''
class ModelOfHomePlus:
    
    def __init__(self) -> None:
        self._flag :str= "homeplus"
        self._url :str= "https://front.homeplus.co.kr/totalsearch/total/popular.json"
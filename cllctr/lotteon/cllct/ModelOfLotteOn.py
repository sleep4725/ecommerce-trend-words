from urllib.parse import urlencode
'''
롯데온
'''
class ModelOfLotteOn:
    
    def __init__(self) -> None:
        self._flag :str= "lotte-on"
        self._url :str= "https://www.lotteon.com/search/render/render.ecn?"
        self._params = urlencode({
            "render": "nqapi"
            , "collection_id": "9"
            , "platform": "pc"
            , "u9": "hotKeywordContent"
            , "u10": "N"
        })
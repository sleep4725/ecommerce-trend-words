from urllib.parse import urlencode
'''
CJ온스타일
@author
'''
class ModelOfCJOnStyle:
    
    def __init__(self) -> None:
        self._flag :str= "cj-onstyle"
        self._url :str= "https://search.cjonstyle.com/search-web/search/topSearchKeyword/topKeyword.json?"
        self._params = urlencode({
            "callback": "jQuery11230958468326984051_1673338827602",
            "mallCd": "001",
            "_": "1673338827604"
        })
from urllib.parse import urlencode
'''
11번가
@author JunHyeon.Kim
'''
class ModelOfElevenThStree:
    
    def __init__(self) -> None:
        self._flag :str= "11th-stree"
        self._url :str= "https://www.11st.co.kr/AutoCompleteAjaxAction.tmall?"
        self._params = urlencode({
            "method": "getKeywordRankJson"
            , "type": "hot"
            , "isSSL": "Y"
            , "rankCnt": "20"
            , "callback": "fetchSearchRanking"
        })
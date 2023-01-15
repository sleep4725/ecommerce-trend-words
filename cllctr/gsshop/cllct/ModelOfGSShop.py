from urllib.parse import urlencode
'''
gsshop
@author JunHyeon.Kim
@date 20230112
@version 0.1
'''
class ModelOfGSShop:
    
    def __init__(self) -> None:
        self._flag :str= "gsshop"
        self._url :str= "https://m.gsshop.com/search/hotKeyword?rownum=20"
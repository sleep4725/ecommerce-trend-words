import os
import sys
CURRENT_FILE_PATH :str= os.path.abspath(os.path.dirname(__file__))

for _ in range(3):
    CURRENT_FILE_PATH :str= os.path.dirname(CURRENT_FILE_PATH)

sys.path.append(CURRENT_FILE_PATH)

import requests 
from requests.models import Response
import bs4
import json
from bs4 import BeautifulSoup
from dataclasses import asdict
from elasticsearch.helpers import bulk 
from elasticsearch import Elasticsearch

from skeleton.Template import Template
from skeleton.Element import Element

from cllctr.common.Common import Common
from cllctr.gsshop.cllct.ModelOfGSShop import ModelOfGSShop
from es.EsCommon import EsCommon
from es.EsClient import EsClient
from util.TimeUtil import TimeUtil

''' gsfresh 
@author JunHyeonKim
@date 20230108
@version 0.1
'''
class CllctOfGSShop(Template, ModelOfGSShop, EsCommon):
    
    def __init__(self) -> None:
        ModelOfGSShop.__init__(self)
        EsCommon.__init__(self)
        
    def step_crawl_start(self):
        '''
        :param:
        :return:
        '''
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        response :Response= requests.get(self._url, headers=header)
        if Common.is_request_good(response= response):
            bs_object = BeautifulSoup(response.text, "html.parser")
            if bs_object:
                self.get_words(bs_object)
        else:
            print("request error")
                
    def get_words(self, bs_object: BeautifulSoup):
        '''
        :param:
        :return:
        '''
        result = bs_object.text
        result_list :list[dict]= dict(json.loads(result))["list"]
        
        for rank, txt in enumerate(result_list):
            element = Element()
            element.current_rank :int= rank + 1
            element.keyword :str= txt["term"]
            element.current_time :str= TimeUtil.get_current_time()
            element.flag :str= self._flag
            self._action.append(
                {
                    "_index": self._index
                    , "_id": element.flag + "_" + element.keyword
                    , "_source": dict(asdict(element))
                })
        
    def words_data_insert_to_es(self):
        '''
        :param:
        :return:
        '''
        Common.es_insert(
            action= self._action, 
            es= EsClient.get_es_client()
        ) 
                
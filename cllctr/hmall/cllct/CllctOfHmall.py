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
from cllctr.hmall.cllct.ModelOfHmall import ModelOfHmall
from es.EsCommon import EsCommon
from es.EsClient import EsClient
from util.TimeUtil import TimeUtil

'''H-mall 
@author JunHyeonKim
@date 20230108
@version 0.1
'''
class CllctOfHmall(Template, ModelOfHmall, EsCommon):
    
    def __init__(self) -> None:
        ModelOfHmall.__init__(self)
        EsCommon.__init__(self)
        
    def step_crawl_start(self):
        '''
        :param:
        :return:
        '''
        response :Response= requests.get(self._url)
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
        elements :list[dict]= dict(json.loads(bs_object.text))["popScwd"]
        for e in elements:
            element = Element()
            element.keyword :str= e["keyword"]
            element.current_rank :int= e["ranking"]
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
                
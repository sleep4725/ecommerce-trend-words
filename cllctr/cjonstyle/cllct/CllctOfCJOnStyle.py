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
from cllctr.cjonstyle.cllct.ModelOfCJOnStyle import ModelOfCJOnStyle
from es.EsCommon import EsCommon
from es.EsClient import EsClient
from util.TimeUtil import TimeUtil

''' CJ온스타일
@author JunHyeonKim
@date 20230108
@version 0.1
'''
class CllctOfCJOnStyle(Template, ModelOfCJOnStyle, EsCommon):
    
    def __init__(self) -> None:
        ModelOfCJOnStyle.__init__(self)
        EsCommon.__init__(self)
        
    def step_crawl_start(self):
        '''
        :param:
        :return:
        '''
        response :Response= requests.get(self._url + self._params)
        if Common.is_request_good(response= response):
            bs_object = BeautifulSoup(response.text, "html.parser")
            if bs_object:
                print(type(bs_object))
                self.get_words(bs_object)
                
    def get_words(self, bs_object: BeautifulSoup):
        '''
        :param:
        :return:
        '''
        rank = dict(json.loads(str(bs_object.text).lstrip("jQuery11230958468326984051_1673338827602(").rstrip(");")))
        for e in rank["result"]:
            element = Element()
            element.keyword = e["title"]
            element.current_rank = e["dispOrder"]
            element.current_time = TimeUtil.get_current_time()
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
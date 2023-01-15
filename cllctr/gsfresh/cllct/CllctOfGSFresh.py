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
from cllctr.gsfresh.cllct.ModelOfGSFresh import ModelOfGSFresh
from es.EsCommon import EsCommon
from es.EsClient import EsClient
from util.TimeUtil import TimeUtil

''' gsfresh 
@author JunHyeonKim
@date 20230108
@version 0.1
'''
class CllctOfGSFresh(Template, ModelOfGSFresh, EsCommon):
    
    def __init__(self) -> None:
        ModelOfGSFresh.__init__(self)
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
        tranding_keyword :bs4.element.Tag= bs_object.select_one(
            "section.trending_keyword" 
            + " > "
            + "div.keyword"
            + " > "
            + "ul.swiper-wrapper"
        )
        if tranding_keyword:
            tranding_keywords :bs4.element.ResultSet= tranding_keyword.select("li.swiper-slide")
            
            for t in tranding_keywords:
                a_tag :bs4.element.Tag= t.select_one("a")
          
                if a_tag:
                    keyword_rank = a_tag.select_one("em")
                    keyword_txt = a_tag.select_one("span")
                    if keyword_rank and keyword_txt:
                        element = Element()
                        element.keyword = str(keyword_txt.text).strip()
                        element.current_rank = int(str(keyword_rank.text).strip())
                        element.current_time :str= TimeUtil.get_current_time()
                        element.flag :str= self._flag
                        self._action.append(
                            {
                                "_index": self._index
                                , "_id": element.flag + "_" + element.keyword
                                , "_source": dict(asdict(element))
                            })
                    else:
                        ''''''
                else:
                    ''''''
        else:
            ''''''
        
        print(self._action)
              
    def words_data_insert_to_es(self):
        '''
        :param:
        :return:
        '''
        Common.es_insert(
            action= self._action, 
            es= EsClient.get_es_client()
        ) 
                
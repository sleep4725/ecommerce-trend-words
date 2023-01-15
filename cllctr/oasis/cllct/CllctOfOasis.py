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
from cllctr.oasis.cllct.ModelOfOasis import ModelOfOasis
from es.EsCommon import EsCommon
from es.EsClient import EsClient
from util.TimeUtil import TimeUtil

''' 롯데온
@author JunHyeonKim
@date 20230108
@version 0.1
'''
class CllctOfOasis(Template, ModelOfOasis, EsCommon):
    
    def __init__(self) -> None:
        ModelOfOasis.__init__(self)
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
                print(type(bs_object))
                self.get_words(bs_object)
        
        response.close()
             
    def get_words(self, bs_object: BeautifulSoup):
        '''
        :param:
        :return:
        '''
        li_tags :bs4.element.ResultSet= bs_object.select("li")
        for l in li_tags:
            element = Element()
            a_tag :bs4.element.Tag= l.select_one("a")
            if a_tag:
                em_tag = a_tag.select_one("em")
                if em_tag:
                    word_rank :str= str(em_tag.text).strip()
                    word_txt :str= str(a_tag.text).strip()
                    result_word_txt :str= word_txt.lstrip(word_rank)
                    element.keyword :str= result_word_txt
                    element.current_rank :int= int(word_rank)
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
        
    def words_data_insert_to_es(self):
        '''
        :param:
        :return:
        '''
        Common.es_insert(
            action= self._action, 
            es= EsClient.get_es_client()
        )  
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
from cllctr.lotteon.cllct.ModelOfLotteOn import ModelOfLotteOn
from es.EsCommon import EsCommon
from es.EsClient import EsClient
from util.TimeUtil import TimeUtil

''' 롯데온
@author JunHyeonKim
@date 20230108
@version 0.1
'''
class CllctOfLotteOn(Template, ModelOfLotteOn, EsCommon):
    
    def __init__(self) -> None:
        ModelOfLotteOn.__init__(self)
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
        kyw_cnt_are :bs4.element.Tag= bs_object.select_one(
            "div.srchHotKeywordContentsArea"+ 
            " > " + 
            "div.srchRankingArea"
        )
        if kyw_cnt_are:
            srch_ranking_box :bs4.element.ResultSet= kyw_cnt_are.select("div.srchRankingBox")
            for s in srch_ranking_box:
                srch_ranking_list :bs4.element.Tag= s.select_one("ul.srchRankingList")
                if srch_ranking_list:
                    srch_rank_items :bs4.element.ResultSet= srch_ranking_list.select("li > a.srchRankItem")
                    for item in srch_rank_items:
                        if item:
                            element = Element()
                            element.keyword :str= str(item.select_one("span.srchRankTitle").text).strip()
                            element.current_rank :int= int(item.select_one("strong.srchRankNum").text)
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
            
    def words_data_insert_to_es(self):
        '''
        :param:
        :return:
        '''
        Common.es_insert(
            action= self._action, 
            es= EsClient.get_es_client()
        )  
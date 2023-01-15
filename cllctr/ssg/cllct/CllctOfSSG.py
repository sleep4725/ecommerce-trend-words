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
from cllctr.ssg.cllct.ModelOfSSG import ModelOfSSG
from es.EsCommon import EsCommon
from es.EsClient import EsClient
from util.TimeUtil import TimeUtil

'''ssg 
@author JunHyeonKim
@date 20230109
@version 0.1
'''
class CllctOfSSG(Template, ModelOfSSG, EsCommon):
    
    def __init__(self) -> None:
        ModelOfSSG.__init__(self)
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
                
    def get_words(self, bs_object: BeautifulSoup):
        '''
        :param:
        :return:
        '''
        cmjump_rank_lst :bs4.element.Tag= bs_object.select_one(
            "div#cmjumpRank.cmjump_rank.renew.notranslate" + 
            " > " +
            "div.cmjump_totalrank" + 
            " > " + 
            "div.cmjump_totalrank_cont" + 
            " > " +
            "ul.cmjump_rank_lst.bx_slide"
        )
        
        if cmjump_rank_lst:
            a_tags :bs4.element.ResultSet= cmjump_rank_lst.select(
                "li.cmjump_rank_item" + 
                " > " +
                "a"
            )
            for r in a_tags:
                rank_num_tag :bs4.element.Tag= r.select_one("span.cmjump_rank_num")
                txt_tag :bs4.element.Tag= r.select_one("span.cmjump_rank_tx")

                if rank_num_tag and txt_tag:
                    element = Element()
                    rank_num_v :int= int(str(rank_num_tag.text).rstrip("."))
                    txt_v :str= str(txt_tag.text).strip()
                    
                    element.flag = self._flag
                    element.keyword = txt_v
                    element.current_rank = rank_num_v
                    element.current_time = TimeUtil.get_current_time()
                    self._action.append(
                                {
                                    "_index": self._index
                                    , "_id": element.flag + "_" + element.keyword
                                    , "_source": dict(asdict(element))
                                })
                else:
                    '''
                    '''
        else:
            ''' cmjump_rank_lst == null
            '''
                
    def words_data_insert_to_es(self):
        '''
        :param:
        :return:
        '''
        Common.es_insert(
            action= self._action, 
            es= EsClient.get_es_client()
        )    
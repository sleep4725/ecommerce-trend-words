from requests.models import Response
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class Common:
    
    @classmethod
    def is_request_good(cls, response:Response):
        '''
        :param response:
        '''
        
        if response.status_code == 200: return True
        else:
            print(response.text) 
            return False
        
    @classmethod 
    def es_insert(cls, action: list[dict], es: Elasticsearch):
        '''
        :param:
        :return:
        '''            
        try:
                
            bulk(es, action)
        except:
            print("bulk insert fail !!")
        else:
            print("bulk insert success !!") 

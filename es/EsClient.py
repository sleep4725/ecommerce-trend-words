import os 
PROJ_ROOT_DIR :str = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
import yaml

from elasticsearch import Elasticsearch 

'''
@author JunHyeon.Kim
@date 20221209
'''
class EsClient:
    
    @classmethod 
    def get_es_client(clsstr)-> Elasticsearch:
        '''
        :param deploy:
        :return:
        '''
        global PROJ_ROOT_DIR
        print(f"PROJ_ROOT_DIR: {PROJ_ROOT_DIR}")
        es_conn_info: str = os.path.join(PROJ_ROOT_DIR, "conf/es-conn.yaml")
        is_file_exists: bool = os.path.exists(es_conn_info)
        
        if is_file_exists:
            with open(es_conn_info, "r", encoding="utf-8") as es_info:
                es_conn :dict[str, object]= yaml.safe_load(es_info)
                es_info.close()
                
                port: int = es_conn["es-port"]
                schema: str = es_conn["es-schema"]
                hosts: list[str] = [
                    f"{schema}://{h}:{port}" for h in es_conn["es-host"]
                ]
                print(f"host : {hosts} *****************")
                es_client: Elasticsearch = Elasticsearch(hosts)
                print(es_client.cluster.health())
                return es_client
        else:
            raise FileNotFoundError
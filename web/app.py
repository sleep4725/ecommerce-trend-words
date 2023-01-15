import os
import sys
import json
PROJ_ROOT_DIR :str= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJ_ROOT_DIR)

from es.EsClient import EsClient

from elasticsearch import Elasticsearch
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/tst")
def tst():
    """"""
     
    es_client :Elasticsearch= EsClient.get_es_client()
    key_dicts = {
        "cj-onstyle": [],
        "oasis": [],
        "ssg": [],
        "gsfresh": [],
        "gsshop": [],
        "hmall": [],
        "homeplus": [],
        "lotte-on": [],
        "11th-stree": []
    }
    for k in key_dicts.keys():
        query :dict[str, object]= {
            "size": 10,
            "query": {
                "term": {
                    "flag": {
                        "value": k 
                    }
                }
            }
        }
        
        response = es_client.search(
            index="popular-search-terms", 
            body=query
        )
        
        result :list[dict]= list()
        
        json_response = json.loads(json.dumps(response["hits"]["hits"], ensure_ascii=False))
        for element in json_response:
            source :dict[str, object]= element["_source"]
            result.append({
                "keyword": source["keyword"]
                , "current_rank": source["current_rank"]
            })
    
        sorted_list = sorted(result, key= lambda x: x["current_rank"])
    
        key_dicts[k].extend(sorted_list) 
     
    return render_template("rank.html", word_list= key_dicts)
    
@app.route("/")
def index():
    return "hello world"

if __name__ == "__main__":
    app.run(
        port = 4099, 
        host = "127.0.0.1",
        debug = True
    )
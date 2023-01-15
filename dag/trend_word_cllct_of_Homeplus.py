''' 11번가
@author JunHyeon.Kim 
@date 20230114
'''
import os

import os
from datetime import datetime
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta 

# -------------------------------------------------
# Timezone setup
local_tz = pendulum.timezone("Asia/Seoul")
# -------------------------------------------------
FLAG :str= "homeplus"

DAG_ID, _ = os.path.splitext(os.path.basename(__file__))
print(DAG_ID)

default_args = {
    'owner': 'airflow',
    'catchup': False,
    'execution_timeout': timedelta(hours=6),
    'depends_on_past': False,
}

with DAG (
    DAG_ID
    , schedule_interval = "@once"
    , start_date = datetime(2023, 1, 13, tzinfo= local_tz)
    , default_args = default_args
    , tags = ["JunHyeon.Kim", "trend-ranking", FLAG]
) as dag:
    run_script= "{py_interpreter} {py_file}".format(
        py_interpreter='/opt/homebrew/bin/python3.10'
	    ,py_file='/Users/kimjunhyeon/popular-search-terms/cllctr/homeplus/HomePlusApplication.py'
    )
    
    trend_rank_word_of_homeplus = BashOperator(
        task_id= f'trend-rank-word-{FLAG}'
        , bash_command= run_script
        , dag= dag
    )
    
    trend_rank_word_of_homeplus 
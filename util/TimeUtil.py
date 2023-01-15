import datetime

'''
'''
class TimeUtil:
    
    @classmethod 
    def get_current_time(cls)\
            -> str:
        '''
        '''
        dt_now :datetime.datetime= datetime.datetime.now()
        dt_now_format :str= dt_now.strftime("%Y-%m-%d %H:%M")
        return dt_now_format
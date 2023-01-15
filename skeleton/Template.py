from abc import *
class Template(metaclass=ABCMeta):

    @abstractmethod
    def step_crawl_start(self):
        pass
     
    @abstractmethod
    def get_words(self):
        pass
    
    @abstractmethod
    def words_data_insert_to_es(self):
        pass
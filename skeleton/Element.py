from dataclasses import dataclass 

@dataclass
class Element:
    flag :str= ""
    keyword :str= ""
    current_rank :int= 0
    search_count :int= 0
    current_time :str=""
from cllct.CllctOfCJOnStyle import CllctOfCJOnStyle 

'''CJ온스타일
'''
def main():
    o = CllctOfCJOnStyle()
    o.step_crawl_start()
    o.words_data_insert_to_es() 
if __name__ == "__main__":
    main()
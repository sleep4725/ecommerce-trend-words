from cllct.CllctOfLotteOn import CllctOfLotteOn

''' 롯데온
'''
def main():
    o = CllctOfLotteOn()
    o.step_crawl_start()
    o.words_data_insert_to_es()
if __name__ == "__main__":
    main()
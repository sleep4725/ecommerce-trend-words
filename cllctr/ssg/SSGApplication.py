from cllct.CllctOfSSG import CllctOfSSG

def main():
    o = CllctOfSSG()
    o.step_crawl_start()
    o.words_data_insert_to_es()
if __name__ == "__main__":
    main()
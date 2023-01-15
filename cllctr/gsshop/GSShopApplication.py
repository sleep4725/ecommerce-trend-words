from cllct.CllctOfGSShop import CllctOfGSShop

def main():
    o = CllctOfGSShop()
    o.step_crawl_start()
    o.words_data_insert_to_es() 
if __name__ == "__main__":
    main()
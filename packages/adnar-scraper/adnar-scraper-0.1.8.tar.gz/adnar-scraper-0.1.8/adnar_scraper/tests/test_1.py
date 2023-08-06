from adnar_scraper.utility.data_loader import DataLoader

k = DataLoader.load_pickle_data(file_path='/media/discoverious/Backup Plus/databases/ver_1/local_database/item_database/shop_detail_scraper/2020_10_4_14_45/process_2.pkl')

for d in k:
    print(d)
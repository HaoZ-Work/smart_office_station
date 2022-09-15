
import pymongo


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    dht_db = client["dht22"]
    print(client.list_database_names())
    recoding = {'name': 'dht', 'temperature': 10, 'humidity': 10,  }
    dht_table = dht_db['user01']
    dht_table.insert_one(recoding)
    print(dht_table.find_one())

if __name__ == main():
    main()
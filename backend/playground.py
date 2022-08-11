from ast import main
import pymongo


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    dht_db = client["dht22"]
    print(client.list_database_names())
    recoding = {'name': 'dht', 'temperature': 1.2, 'humidity': 57.5,  }
    dht_table = dht_db['station01']
    dht_table.insert_one(recoding)

if __name__ == main():
    main()
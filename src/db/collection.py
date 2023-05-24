import pymongo


def init_collection(db_name, collection_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = client.list_database_names()

    # if db_name not in dblist:
    #     raise Exception(f"DB {db_name} not exists")
    db = client[db_name]

    # if collection_name not in db.list_collection_names():
    #     raise Exception(f"Collection {collection_name} not exists")
    return db[collection_name]

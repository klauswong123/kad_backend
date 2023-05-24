from src.db.collection import init_collection
from src.constatns import DB_NAME

COLLECTION_NAME = 'ads'

ad = {
    'logoUrl': 'assets/images/google_logo.png',
    'role': 'Endorser',
    'owner': 'klaus',
    'isMark': False,
    'title': 'new ad',
    'description': 'hello world',
    'price': 2000,
    'req': 'kol, 1000+ followers',
    'ad_id': 'auhuiasd',
    'applier': ['123abc'],
    'tags': ['youtuber', 'movie', 'food']
}


def add_one_ad(data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.insert_one(data)
    if not res.inserted_id:
        raise Exception(f"Data insertion failed in add_one_ad. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    return True


def add_ads(ads):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.insert_many(ads)
    if not res.acknowledged:
        raise Exception(f"Data insertion failed in add_ads. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    return True


def find_ads(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = list(collection.find(query, {'_id': False}))
    return res


def find_one_ad(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.find_one(query, {'_id': False})
    return res


def update_one_ad(query, data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.update_one(query, data)
    if not res.acknowledged:
        raise Exception(f"Data update failed in update_one_ad. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.modified_count == 1:
        return True
    else:
        return False


def update_ads(query, data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.update_many(query, data)
    if not res.acknowledged:
        raise Exception(f"Data update failed in update_ads. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.modified_count >= 1:
        return True
    else:
        return False


def delete_one_ad(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.delete_one(query)
    if not res.acknowledged:
        raise Exception(f"Data delete failed in delete_one_ad. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.deleted_count == 1:
        return True
    else:
        return False


def delete_ads(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.delete_many(query)
    if not res.acknowledged:
        raise Exception(f"Data delete failed in delete_ads. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.deleted_count >= 1:
        return True
    else:
        return False

from src.db.collection import init_collection
from src.constatns import DB_NAME

COLLECTION_NAME = 'notification'

def add_one_notification(data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.insert_one(data)
    if not res.inserted_id:
        raise Exception(f"Data insertion failed in add_one_notification. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    return True


def add_notification(notification):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.insert_many(notification)
    if not res.acknowledged:
        raise Exception(f"Data insertion failed in add_notification. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    return True


def find_notification(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = list(collection.find(query, {'_id': False}))
    return res


def find_one_notification(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.find_one(query, {'_id': False})
    return res


def update_one_notification(query, data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.update_one(query, data)
    if not res.acknowledged:
        raise Exception(f"Data update failed in update_one_notification. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.modified_count == 1:
        return True
    else:
        return False


def update_notification(query, data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.update_many(query, data)
    if not res.acknowledged:
        raise Exception(f"Data update failed in update_notification. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.modified_count >= 1:
        return True
    else:
        return False


def delete_one_notification(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.delete_one(query)
    if not res.acknowledged:
        raise Exception(f"Data delete failed in delete_one_notification. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.deleted_count == 1:
        return True
    else:
        return False


def delete_notification(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.delete_many(query)
    if not res.acknowledged:
        raise Exception(f"Data delete failed in delete_notification. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.deleted_count >= 1:
        return True
    else:
        return False

from src.db.collection import init_collection
from src.constatns import DB_NAME

COLLECTION_NAME = 'users'


# user = {
#     'name': 'kad',
#     'email': 'assets/images/google_logo.png',
#     'phone': 'Endorser',
#     'password': 'klaus',
#     'user_id': 'abc123',
#     'type': 'personal',
#     'tags': ['youtuber', 'movie', 'food']
# }


def add_one_user(data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.insert_one(data)
    if not res.inserted_id:
        raise Exception(f"Data insertion failed in add_one_user. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    return True


def add_ads(users):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.insert_many(users)
    if not res.acknowledged:
        raise Exception(f"Data insertion failed in add_ads. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    return True


def find_users(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = list(collection.find(query, {'_id': False}))
    return res


def find_one_user(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.find_one(query, {'_id': False})
    return res


def update_one_user(query, data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.update_one(query, data)
    if not res.acknowledged:
        raise Exception(f"Data update failed in update_one_user. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.modified_count == 1:
        return True
    else:
        return False


def update_users(query, data):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.update_many(query, data)
    if not res.acknowledged:
        raise Exception(f"Data update failed in update_users. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.modified_count >= 1:
        return True
    else:
        return False


def delete_one_user(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.delete_one(query)
    if not res.acknowledged:
        raise Exception(f"Data delete failed in delete_one_user. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.deleted_count == 1:
        return True
    else:
        return False


def delete_users(query):
    collection = init_collection(DB_NAME, COLLECTION_NAME)
    res = collection.delete_many(query)
    if not res.acknowledged:
        raise Exception(f"Data delete failed in delete_users. DB: {DB_NAME}, Collection: {COLLECTION_NAME}")
    if res.deleted_count >= 1:
        return True
    else:
        return False


def update_user_list_property(data_key, query, data, remove_when_duplicate):
    user = find_one_user(query=query)
    if data_key not in user:
        user[data_key] = []
    data_list = user[data_key]
    if data not in data_list:
        if remove_when_duplicate:
            data_list.remove(data)
    else:
        data_list.push(data)
    new_data = {
        data_key: data
    }
    update_one_user(query=query, data=new_data)

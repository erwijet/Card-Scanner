from pymongo import MongoClient

def insert_card_into_owned_collection(cardname: str):
    CONN_STRING = '< your mongoDB url here :) >'

    client = MongoClient(CONN_STRING)
    db = client['cardlib']

    owned = db.owned
    post_data = {
        'name': cardname
    }
    _ = owned.insert_one(post_data)
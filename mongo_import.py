from pymongo import MongoClient

def insert_card_into_owned_collection(cardname: str):
    CONN_STRING = 'mongodb://dbo:honeyTSH207980@ds127015.mlab.com:27015/cardlib'

    client = MongoClient(CONN_STRING)
    db = client['cardlib']

    owned = db.owned
    post_data = {
        'name': cardname
    }
    _ = owned.insert_one(post_data)
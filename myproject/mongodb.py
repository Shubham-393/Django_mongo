from pymongo import MongoClient
def get_db():

    connection_string = "mongodb+srv://youtubepy:youtubepy@cluster0.hlekbr4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(connection_string)

    database1 = client['database1']

    return database1
from pymongo import MongoClient
import certifi

MONGO_URY = 'mongodb+srv://lairedislas04:LaiP04@cluster0.sp1wiud.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URY, tlsCAFile=ca)
        db=client["DataBasePPLaired"]
    except ConnectionError:
        print("ERROR")
    return db
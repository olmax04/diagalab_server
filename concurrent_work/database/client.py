from typing import List

from pymongo import MongoClient

from concurrent_work.database.schemas.city import City
from controllers.timestamp_controller import create_timestamp

uri = "mongodb+srv://root:root@databasecluster.j88rtik.mongodb.net/?retryWrites=true&w=majority&appName=DatabaseCluster"
client = MongoClient(uri)
db = client['diag_parser']

def log_message(message: str):
    db.logs.insert_one({"msg": message, "timestamp": create_timestamp()})


def add_analyze(analyze):
    db.analyses.update_one({'source': analyze.source, 'city': analyze.city, 'name': analyze.name},
                           {'$set': analyze.__dict__}, upsert=True)
    log_message(f"Analyze on source {analyze.source} created, city: {analyze.city}, name: {analyze.name}")


def get_cities_alab() -> List[City]:
    return [City(item['name']) for item in list(db.cities_alab.find())]


def get_cities_diag() -> List[City]:
    return [City(item['name']) for item in list(db.cities_diag.find())]


if __name__ == "__main__":
    print(get_cities_diag())

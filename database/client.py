from typing import List

from pymongo import MongoClient

from controllers.timestamp_controller import create_timestamp

uri = "mongodb+srv://root:root@databasecluster.j88rtik.mongodb.net/?retryWrites=true&w=majority&appName=DatabaseCluster"
client = MongoClient(uri)
db = client['diag_parser']


class City:
    city: str

    def __init__(self, city: str):
        self.city: str = city

    def __str__(self):
        return self.city


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


def create_source_log(source: str, city: str):
    db.statistic.insert_one(
        {"ParsingStartTime": create_timestamp(), "ParsingFinishTime": None, "City": city, "Source": source,
         "ParcedPriceNum": 0, "OfflineOnlyPrices": 0, "NotAavailablePrices": 0})


def update_source_log(source: str, city: str):
    record = list(db.statistic.find({"City": city, "Source": source}).sort({"$natural": -1}).limit(1))[0]
    records = list(db.analyses.find({"source": source, "city": city}))
    ParcedPriceNum = len(records)
    OfflineOnlyPrices = len([record for record in records if record["status"] == "offline_only"])
    NotAavailablePrices = len([record for record in records if record["status"] == "not_available"])
    db.statistic.update_one({"_id": record["_id"]}, {
        "$set": {"ParsingFinishTime": create_timestamp(), "ParcedPriceNum": ParcedPriceNum,
                 "OfflineOnlyPrices": OfflineOnlyPrices,
                 "NotAavailablePrices": NotAavailablePrices}})

def insert_town():
    cities = [
        "Bielsko-Biała", "Bydgoszcz", "Bytom", "Częstochowa", "Człuchów", "Dobczyce",
        "Gdańsk", "Gdynia", "Gliwice", "Głowno", "Gorzów Wielkopolski", "Grudziądz",
        "Jaworzno", "Katowice", "Kołobrzeg", "Koszalin", "Kościerzyna", "Kożuchów",
        "Kraków", "Lublin", "Łowicz", "Łódź", "Międzyrzecz", "Mikołów", "Myślenice",
        "Nowa Sól", "Nysa", "Otmuchów", "Paczków", "Piotrków Trybunalski", "Poznań",
        "Rybnik", "Rzeszów", "Sosnowiec", "Starogard Gdański", "Sulechów", "Świebodzin",
        "Tarnów", "Tczew", "Tomaszów Lubelski", "Toruń", "Tychy", "Warszawa", "Wieliczka",
        "Włocławek", "Wolbrom", "Wołomin", "Wrocław", "Zabrze", "Ząbkowice Śląskie",
        "Zielona Góra", "Żary", "Smolec", "Brodnica", "Skórzewo", "Szczecin", "Bardo", "Rumia"
    ]
    for city in cities:
        db.cities_alab.insert_one({"name": city})
        # db.cities_diag.insert_one({"name": city})

if __name__ == "__main__":
    # update_source_log("Alab", "Warszawa")
    insert_town()
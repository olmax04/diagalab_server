from controllers.timestamp_controller import create_timestamp


class Analyze:

    def __init__(self, source, city, name, price, url, status, createdAt=None, updatedAt=None):
        self.source = source

        self.city = city

        self.name = name

        self.price = price

        self.url = url

        self.status = status

        self.createdAt = create_timestamp() if createdAt is None else createdAt

        self.updatedAt = create_timestamp() if updatedAt is None else updatedAt

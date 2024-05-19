class City:

    city: str

    def __init__(self, city: str):
        self.city: str = city

    def __str__(self):
        return self.city
from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getAllCountries(self):
        return DAO.getAllCountries()
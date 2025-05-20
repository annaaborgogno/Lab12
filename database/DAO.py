from database.DB_connect import DBConnect

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select distinct gr.Country as country 
                    from go_retailers gr """
        cursor.execute(query)

        for row in cursor:
            res.append(row["country"])
        cursor.close()
        conn.close()
        return res
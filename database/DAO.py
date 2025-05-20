from database.DB_connect import DBConnect
from model.arco import Arco
from model.retailer import Retailer

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

    @staticmethod
    def getAllNodes(country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select *
                    from go_retailers gr 
                    where gr.Country = %s"""
        cursor.execute(query, (country,))

        for row in cursor:
            res.append(Retailer(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEdges(year, country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select least(gr.Retailer_code, gr2.Retailer_code) as codRetailer1, greatest(gr.Retailer_code, gr2.Retailer_code) as codRetailer2, count(distinct gds.Product_number) as peso
                    from go_retailers gr, go_daily_sales gds, go_retailers gr2, go_daily_sales gds2 
                    where gr.Retailer_code = gds.Retailer_code 
                    and gr2.Retailer_code = gds2.Retailer_code 
                    and year (gds.`Date`) = %s
                    and gds.Product_number = gds2.Product_number 
                    and year (gds.Date) = year (gds2.Date) 
                    and gds.Retailer_code != gds2.Retailer_code 
                    and gr.Country = %s
                    and gr.Country = gr2.Country
                    group by least(gr.Retailer_code, gr2.Retailer_code), greatest(gr.Retailer_code, gr2.Retailer_code)"""
        cursor.execute(query, (year, country,))

        for row in cursor:
            res.append(Arco(**row))
        cursor.close()
        conn.close()
        return res
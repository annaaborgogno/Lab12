from database.DB_connect import DBConnect
from model.edge import Edge
from model.retailer import Retailer

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getCountries():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select distinct gr.Country as country
                    from go_retailers gr """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["country"])
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(gds.`Date`) as year
                    from go_daily_sales gds 
                    order by year(gds.`Date`) ASC"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getNodes(country):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr 
                    where gr.Country = %s"""
        cursor.execute(query, (country, ))

        res = []
        for row in cursor:
            res.append(Retailer(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdges(country, year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select least(gr1.Retailer_code, gr2.Retailer_code) as Retailer_code1, greatest(gr1.Retailer_code, gr2.Retailer_code) as Retailer_code2, count(distinct gds1.Product_number) as peso
from go_retailers gr1, go_retailers gr2, go_daily_sales gds1, go_daily_sales gds2
where gr1.Retailer_code = gds1.Retailer_code 
and gr2.Retailer_code = gds2.Retailer_code
and gr1.Country = gr2.Country
and gr1.Country = %s
and year(gds1.Date) = year(gds2.Date)
and year(gds1.Date) = %s
and gr1.Retailer_code < gr2.Retailer_code
and gds1.Product_number = gds2.Product_number
group by least(gr1.Retailer_code, gr2.Retailer_code), greatest(gr1.Retailer_code, gr2.Retailer_code)"""
        cursor.execute(query, (country, year))

        res = []
        for row in cursor:
            res.append(Edge(**row))
        cursor.close()
        conn.close()
        return res
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.idMap = {}
        self._nodes = []
        self._graph = nx.Graph()

    def getAllCountries(self):
        return DAO.getAllCountries()

    def addEdges(self, year, country):
        edges = DAO.getAllEdges(year, country)
        for e in edges:
            u = self.idMap[e.codRetailer1]
            v = self.idMap[e.codRetailer2]
            self._graph.add_edge(u,v, weight=e.peso)
            
    def buildGraph(self, year, country):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(country)
        for n in self._nodes:
            self.idMap[n.Retailer_code] = n
        self._graph.add_nodes_from(self._nodes)
        self.addEdges(year, country)

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def getPeso(self, u, v):
        for u, v, data in self._graph.edges(data=True):
            return self._graph[u][v]["weight"]
    
    def getVolume(self):
        volumi = {}
        for n in self._graph.nodes:
            volume = 0
            for n1 in self._graph.neighbors(n):
                peso = self.getPeso(n, n1)
                volume += peso
            volumi[n] = volume
            print(f"Il nodo {n} ha volume {volume}")
        return volumi
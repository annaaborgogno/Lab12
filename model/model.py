import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._years = []
        self._countries = []
        self._nodes = []
        self._edges = []
        self._idMap = {}
        self._graph = nx.Graph()
        self._bestPath = []
        self._maxWeight = 0

    def getBestPath(self, num):
        self._bestPath = []
        self._maxWeight = 0

        for start in self._graph.nodes:
            parziale = [start]
            self._ricorsione(start, parziale, num)

        return self._bestPath, self._maxWeight

    def _ricorsione(self, start, parziale, num):
        if len(parziale) == num:  # ciclo composto da esattamente n archi
            lastNode = parziale[-1]
            if self._graph.has_edge(lastNode, start):
                parziale.append(start)
                if self.getMaxWeight(parziale) > self._maxWeight:
                    self._maxWeight = self.getMaxWeight(parziale)
                    self._bestPath = copy.deepcopy(parziale)
                parziale.pop()  # rimuove il nodo iniziale dopo la verifica
            return

        lastNode = parziale[-1]
        for n in self._graph.neighbors(lastNode):
            if n not in parziale and n != start:  # verifica che non ci siano ripetizioni, tranne per l'inizio e la fine
                parziale.append(n)
                self._ricorsione(start, parziale, num)
                parziale.pop()

    def getMaxWeight(self, listOfNodes):
        pesoTot = 0
        for i in range(0, len(listOfNodes) - 1):
            pesoTot += self._graph[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return pesoTot

    def getYears(self):
        self._years = DAO.getYears()
        return self._years

    def getCountries(self):
        self._countries = DAO.getCountries()
        return self._countries

    def getNodes(self, country):
        self._nodes = DAO.getNodes(country)
        return self._nodes

    def buildGraph(self, country, year):
        self._graph.clear()
        self._nodes = []
        self._edges = []
        self.getNodes(country)
        self._graph.add_nodes_from(self._nodes)
        for n in self._nodes:
            self._idMap[n.Retailer_code] = n
        self.addAllEdges(country, year)
        return self._graph


    def getGraphDetails(self):
        nNodes = self._graph.number_of_nodes()
        nEdges = self._graph.number_of_edges()
        return nNodes, nEdges

    def addAllEdges(self, country, year):
        self._edges = DAO.getEdges(country, year)
        for e in self._edges:
            if e.Retailer_code1 in self._idMap and e.Retailer_code2 in self._idMap:
                u = self._idMap[e.Retailer_code1]
                v = self._idMap[e.Retailer_code2]
                self._graph.add_edge(u, v, weight=e.peso)

    def getVolumi(self):
        res = {}
        for n in self._nodes:
            peso = 0
            for n1 in self._graph.neighbors(n):
                if self._graph.has_edge(n, n1):
                    peso += self._graph[n][n1]["weight"]
            res[n] = peso
        res_ordinato = dict(sorted(res.items(), key=lambda x: x[1], reverse=True))
        return res_ordinato
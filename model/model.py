import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.idMap = {}
        self._nodes = []
        self.volumi = {}
        self._graph = nx.Graph()
        self._bestPath = []
        self._maxWeight = 0

    def getBestPath(self, n):
        self._bestPath = []
        self._maxWeight = 0

        for start in self._graph.nodes:
            parziale = [start]
            self._ricorsione(start, parziale, n)

        return self._bestPath, self._maxWeight

    def _ricorsione(self, start, parziale, n):
        if len(parziale) == n: #ciclo composto da esattamente n archi
            lastNode = parziale[-1]
            if self._graph.has_edge(lastNode, start):
                parziale.append(start)
                if self.getMaxWeight(parziale) > self._maxWeight:
                    self._maxWeight = self.getMaxWeight(parziale)
                    self._bestPath = copy.deepcopy(parziale) #rimuove il nodo iniziale dopo la verifica
                parziale.pop()
            return

        lastNode = parziale[-1]
        for n in self._graph.neighbors(lastNode):
            if n not in parziale and n != start: #verifica che non ci siano ripetizioni, tranne per l'inizio e la fine
                parziale.append(n)
                self._ricorsione(start, parziale, n)
                parziale.pop()

    def getMaxWeight(self, listOfNodes):
        pesoTot = 0
        for i in range(0, len(listOfNodes) -1):
            pesoTot += self.getPeso(listOfNodes[i], listOfNodes[i+1])
        return pesoTot

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
        if self._graph.has_edge(u, v):
            return self._graph[u][v]["weight"]
        else:
            return 0
    
    def getVolume(self):
        self.volumi = {}
        for n in self._graph.nodes:
            volume = 0
            for n1 in self._graph.neighbors(n):
                peso = self.getPeso(n, n1)
                volume += peso
            self.volumi[n] = volume
        return self.volumi
from model.model import Model

m = Model()
m.buildGraph(2015, "France")
print("archi", m.getNumEdges())
print("nodi", m.getNumNodes())
print(m.getVolume())
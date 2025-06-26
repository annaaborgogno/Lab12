import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDDCountries(self):
        self._listCountry = self._model.getAllCountries()
        for c in self._listCountry:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

    def fillDDYears(self):
        self._listYear = [2015, 2016, 2017, 2018]
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(y))


    def handle_graph(self, e):
        year = self._view.ddyear.value
        country = self._view.ddcountry.value

        if year is None or country is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare tutti i parametri!", color="red"))
            self._view.update_page()

        else:
            self._grafo = self._model.buildGraph(year, country)
            nNodes = self._model.getNumNodes()
            nEdges = self._model.getNumEdges()
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente!"))
            self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi e {nEdges} archi"))
            self._view.update_page()

    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        volumi = self._model.getVolume()
        sorted_volumi = sorted(volumi.items(), key=lambda x: x[1], reverse=True)
        for i in sorted_volumi:
            self._view.txtOut2.controls.append(ft.Text(f"{i[0]} ---> {i[1]}"))
        self._view.update_page()

    def handle_path(self, e):
        nInput = self._view.txtN.value

        if nInput == "":
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text(f"Inserire un valore!", color="red"))

        try:
            nInt = int(nInput)
        except ValueError:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text("Il valore inserito non è un intero!", color="red"))
            return

        if nInt < 2:
            self._view.txtOut3.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Devono esserci almeno 2 archi!", color="red"))

        bestPath, maxWeight = self._model.getBestPath(nInt)
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {maxWeight}"))
        for i in range(0, len(bestPath)):
            peso = self._model.getPeso(bestPath[i], bestPath[i+1])
            self._view.txtOut3.controls.append(ft.Text(f"{bestPath[i]} ---> {bestPath[i+1]}: {peso}"))
        self._view.update_page()

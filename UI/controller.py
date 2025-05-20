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
            grafo = self._model.buildGraph(year, country)
            nNodes = self._model.getNumNodes()
            nEdges = self._model.getNumEdges()
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente!"))
            self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nNodes} nodi e {nEdges} archi"))
            self._view.update_page()

    def handle_volume(self, e):
        pass


    def handle_path(self, e):
        pass

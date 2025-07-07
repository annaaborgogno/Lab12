import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []


    def handle_graph(self, e):
        year = self._view.ddyear.value
        if year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un anno", color="red"))
            self._view.update_page()
            return
        country = self._view.ddcountry.value
        if country is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare uno stato", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(country, year)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato", color="green"))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}, numero di archi {nEdges}"))
        self._view.update_page()

    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text("I volumi di vendita sono:"))
        res = self._model.getVolumi()
        for r, p in res.items():
            self._view.txtOut2.controls.append(ft.Text(f"{r.Retailer_name} --> {p}"))
        self._view.update_page()


    def handle_path(self, e):
        pass

    def fillDDYears(self):
        years = self._model.getYears()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))
        self._view.update_page()

    def fillDDCountries(self):
        countries = self._model.getCountries()
        for c in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))
        self._view.update_page()
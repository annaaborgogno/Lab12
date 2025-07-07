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
        numInput = self._view.txtN.value

        if numInput == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire una lunghezza", color="red"))
            return

        try:
            num = int(numInput)
        except ValueError:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text("Inserire un numero intero", color="red"))
            return

        bestPath, bestWeight = self._model.getBestPath(num)
        self._view.txtOut3.controls.append(ft.Text(f"Il percorso migliore di {num} nodi è stato trovato, con peso {bestWeight}", color="green"))
        self._view.txtOut3.controls.append(ft.Text(f"I nodi che lo compongono sono:"))
        for i in range(0, len(bestPath) - 1):
            nodo1 = bestPath[i]
            nodo2 = bestPath[i + 1]
            peso = self._model._graph[nodo1][nodo2]["weight"]
            self._view.txtOut3.controls.append(
                ft.Text(f"{nodo1.Retailer_name} --> {nodo2.Retailer_name} : {peso}")
            )

        self._view.update_page()

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
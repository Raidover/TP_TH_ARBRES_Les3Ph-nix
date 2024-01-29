import networkx as nx
import matplotlib.pyplot as plt
import itertools
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Fonction pour lire un graphe à partir d'un fichier d'arêtes pondérées
def LectureFichier(fichier):
    Graphe = nx.DiGraph()  # Utiliser un graphe orienté
    with open(fichier, 'r', encoding='utf-8') as file:
        for ligne in file:
            elements = ligne.split()
            if len(elements) == 3:
                source, destination, weight = elements
                weight = int(weight)
                Graphe.add_edge(source, destination, weight=weight)
    return Graphe


# Fonction pour trouver le chemin le plus court entre deux nœuds
def CheminPlusCourt(graphe, source, destination):
    try:
        chemin = nx.shortest_path(graphe, source=source, target=destination, weight='weight')
        cout = nx.shortest_path_length(graphe, source=source, target=destination, weight='weight')
        return chemin, cout
    except nx.NetworkXNoPath:
        return None, float('inf')


# Fonction pour résoudre le problème du voyageur de commerce
def PlusCourtCircuit(graphe, pt_depart, pt_livraison):
    # Liste de tous les nœuds de livraison
    ptLivraison = list(pt_livraison)

    # Vérifier si le point de départ est dans le graphe
    if pt_depart not in graphe.nodes():
        print("Erreur : Le point de départ n'est pas dans le graphe !")
        exit()

    # Initialisation de la solution optimale
    chemin_optimal = None
    cout_optimal = float('inf')

    # Générer toutes les permutations possibles des nœuds de livraison
    permutations = itertools.permutations(ptLivraison)

    # Pour chaque permutation, trouver le chemin optimal entre le point de départ et les points de livraison
    for perm in permutations:
        print("permutation:", perm)
        chemin_partiel = [pt_depart]
        cout_partiel = 0

        for i in range(len(perm)):
            destination = perm[i]
            chemin, cout = nx.shortest_path(graphe, source=chemin_partiel[-1], target=destination,
                                            weight='weight'), nx.shortest_path_length(graphe, source=chemin_partiel[-1],
                                                                                      target=destination,
                                                                                      weight='weight')

            if chemin is not None:
                chemin_partiel += chemin[1:]
                cout_partiel += cout
            else:
                # Pas de chemin possible entre les points de livraison, abandonner cette permutation
                break

        # Ajouter manuellement le dernier segment pour revenir au point de départ
        chemin_retour, cout_retour = nx.shortest_path(graphe, source=chemin_partiel[-1], target=pt_depart,
                                                      weight='weight'), nx.shortest_path_length(graphe,
                                                                                                source=chemin_partiel[-1],
                                                                                                target=pt_depart,
                                                                                                weight='weight')
        chemin_partiel += chemin_retour[1:]
        cout_partiel += cout_retour

        # Mettre à jour la solution optimale si le coût est inférieur
        if cout_partiel < cout_optimal:
            cout_optimal = cout_partiel
            chemin_optimal = chemin_partiel

    return chemin_optimal, cout_optimal


# Spécifiez le chemin de votre fichier
cheminfichier = r'C:\Users\lolo7\OneDrive\Documents\Informatique\3eme année\TH_Arbres_Graphes\TP\graphe.txt'
graph = LectureFichier(cheminfichier)  # Appel de la fonction pour lire le graphe

print("Noms des nœuds dans le graphe :", graph.nodes())

# Point de départ (saisi à partir de l'interface utilisateur)
ptDepart = input("Entrez le point de départ : ")

# Vérifier si le point de départ est dans le graphe
if ptDepart not in graph.nodes():
    print("Erreur : Le point de départ n'est pas dans le graphe !")
    exit()

# Demander à l'utilisateur de saisir les points de livraison
PointsLivraisons = input("Entrez les points de livraison séparés par des espaces : ")
PointsLivraisons = PointsLivraisons.split()

# Vérifier si le nombre de points de livraison est supérieur à 6.
if len(PointsLivraisons) > 6:
    print("Erreur : le nombre de points de livraison ne peut pas dépasser 6.")
    # Ajouter d'autres actions à effectuer en cas d'erreur, par exemple, sortir du programme.
    exit()

cheminOptimal, coutOptimal = PlusCourtCircuit(graph, ptDepart, PointsLivraisons)

print("Plus court circuit: ", cheminOptimal)
print("Coût du plus court circuit: ", coutOptimal)

# Création d'un dictionnaire avec les coordonnées des nœuds
guadeloupe_positions = {
    'Abymes': (16.0987, -61.520),
    'Gosier': (16.1552, -61.999),
    'BaieMahault': (15.9830, -61.321),
    'PAP': (16.0808, -61.838),
    'MorneAleau': (16.1255, -61.258),
    'PetitCanal': (16.1870, -61.147),
    'PortLouis': (16.1893, -60.944),
    'AnseBertrand': (16.2570, -60.868),
    'LeMoule': (16.2730, -61.520),
    'SaintFrancois': (16.3221, -61.999),
    'SainteAnne': (16.2300, -61.999),
    'BasseTerre': (15.8427, -62.115),
    'SaintClaude': (15.8891, -61.779),
    'Baillif': (15.8427, -61.8690),
    'VieuxHabitants': (15.8427, -61.655),
    'Bouillante': (15.8427, -61.4545),
    'PointeNoire': (15.8427, -61.205),
    'Deshaies': (15.8427, -60.845),
    'SainteRose': (15.9279, -60.845),
    'Lamentin': (15.9459, -61.124),
    'Gourbeyre': (15.8891, -62.004),
    'TroisRivieres': (15.9330, -62.125),
    'PetitBourg': (15.9839, -61.624),
    'Goyave': (15.9839, -61.8010),
    'Capesterre': (15.9561, -61.9599),
    'VieuxFort': (15.8891, -62.300),
}

# Attribution des positions aux nœuds du graphe
positions = {noeud: guadeloupe_positions[noeud] for noeud in graph.nodes()}

# Affichage du graphe
nx.draw(graph, positions, with_labels=True, node_size=700, node_color="skyblue", font_size=8, font_color="black",
        font_weight="bold", edge_color="gray", linewidths=1, font_family="sans-serif",
        connectionstyle='arc3,rad=0.1', arrowsize=20)

# Affichage des poids des arêtes
LabelPoidsArete = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, positions, edge_labels=LabelPoidsArete)

# Affichage du graphe
plt.show(block=False)
plt.pause(0.1)

# ------------------------------------------ PARTIE TKINTER -----------------------------------------------------------


class Application(tk.Tk):
    def __init__(self, graphE):
        super().__init__()

        self.title("GRAPHE ROUTES DE GUADELOUPE")

        self.graph = graphE
        self.cheminOptimal = None
        self.coutOptimal = None
        self.pointsLivraison = []
        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Graphe originel')
        tab_control.add(tab2, text='Voyageur de commerce')
        tab_control.add(tab3, text='Résultat')

        tab_control.pack(expand=1, fill='both')

        self.display_graph(tab1, self.create_parameters_tab(tab2))
        self.create_parameters_tab(tab2)
        self.create_result_tab(tab3)

    def display_graph(self, tab, entry_depart):
        # Affichage du graphe sur le premier onglet
        figure, ax = plt.subplots(figsize=(10, 6))
        pos = positions

        # Ajout une vérification pour éviter les erreurs si le chemin optimal est None
        if self.cheminOptimal is not None:
            NoeudCircuitOptimal = set(self.cheminOptimal)
        else:
            NoeudCircuitOptimal = set()

        # Affichage des arêtes avec les coûts
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))

        # Affichage des nœuds en vert sauf le point de départ en rouge
        node_colors = [
            'red' if node == self.point_depart.get() else 'green' if node in NoeudCircuitOptimal else 'skyblue' for
            node in self.graph.nodes()]

        nx.draw(self.graph, pos, with_labels=True, connectionstyle='arc3,rad=0.1', edgelist=self.graph.edges(),
                arrowsize=20, ax=ax, node_size=800, node_color=node_colors)

        canvas = FigureCanvasTkAgg(figure, master=tab)
        canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew", padx=10, pady=10)  # Utilisation de grid ici
        canvas.draw()

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)

    def create_parameters_tab(self, tab):
        # Création des widgets pour le deuxième onglet

        lbl_depart = ttk.Label(tab, text="Point de départ:")
        lbl_depart.pack(side=tk.LEFT, padx=10, pady=10)  # Utilisation de pack ici

        self.point_depart = ttk.Entry(tab)
        self.point_depart.pack(side=tk.LEFT, padx=10, pady=10)

        # Ajout du champ de saisie pour les points de livraison
        lbl_livraison = ttk.Label(tab, text="Points de livraison (séparés par des espaces):")
        lbl_livraison.pack(side=tk.LEFT, padx=10, pady=10)

        self.points_livraison_entry = ttk.Entry(tab)
        self.points_livraison_entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour lancer le calcul
        btn_calculer = ttk.Button(tab, text="Lancer", command=self.calculer)
        btn_calculer.pack(side=tk.LEFT, padx=10, pady=10)

    def create_result_tab(self, tab):
        # Affichage du résultat sur le troisième onglet
        # Label pour le coût optimal
        lbl_cout = ttk.Label(tab, text="Coût optimal:")
        lbl_cout.grid(column=0, row=0)

        self.label_cout = ttk.Label(tab, text="")
        self.label_cout.grid(column=1, row=0)

        # Label pour le chemin optimal
        lbl_chemin = ttk.Label(tab, text="Chemin optimal:")
        lbl_chemin.grid(column=0, row=1)

        self.label_chemin = ttk.Label(tab, text="")
        self.label_chemin.grid(column=1, row=1)

        # Ajout d'une Frame pour afficher le graphe dans le même style que l'onglet "Graphe originel"
        frame = ttk.Frame(tab)
        frame.grid(column=0, row=2, columnspan=3)

        self.display_graph(frame, self.create_parameters_tab(self.nametowidget(self.winfo_parent())))

    def calculer(self):
        # Fonction appelée lors du clic sur le bouton "Lancer"
        # récupérer le point de départ depuis le label
        pt_depart = self.point_depart.get()

        # Récupérer les points de livraison depuis le champ de saisie
        points_livraison = self.points_livraison_entry.get().split()

        # Appel la fonction PlusCourtCircuit
        self.cheminOptimal, self.coutOptimal = PlusCourtCircuit(self.graph, pt_depart, points_livraison)

        # Mise à jour de l'affichage sur le troisième onglet
        self.label_cout.config(text=f"Coût optimal: {self.coutOptimal}")
        print("Chemin optimal:", self.cheminOptimal)

        # Mise à jour de l'affichage du chemin optimal
        if self.cheminOptimal is not None:
            chemin_str = ", ".join(self.cheminOptimal)
            self.label_chemin.config(text=f"Chemin optimal: {chemin_str}")
        else:
            self.label_chemin.config(text="Chemin optimal: Aucun chemin trouvé")


cheminfichier = r'C:\Users\lolo7\OneDrive\Documents\Informatique\3eme année\TH_Arbres_Graphes\TP\graphe.txt'
graph = LectureFichier(cheminfichier)
app = Application(graph)
app.mainloop()
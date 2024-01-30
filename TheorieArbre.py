import networkx as nx
import matplotlib.pyplot as plt
import itertools
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Fonction pour lire un graphe orienté à partir d'un fichier texte
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


# Fonction pour résoudre le problème du voyageur de commerce "PlusCourtCircuit"
def PlusCourtCircuit(Graphe, pt_depart, pt_livraison):
    # Liste de tous les nœuds de livraison
    ptLivraison = list(pt_livraison)

    # Vérifier si les zones de saisie ne sont pas vides
    if pt_depart == "" or len(pt_livraison) == 0:
        messagebox.showerror("Erreur", "Point de départ et/ou Points de livraison incorrects.")
        return None, None

    # Vérifier si le point de départ existe dans le graphe
    if pt_depart not in Graphe.nodes():
        messagebox.showerror("Erreur", "Point de départ et/ou Points de livraison incorrects.")
        return None, None

    # Vérifier si tous les points de livraison existent dans le graphe
    if not all(point in Graphe.nodes() for point in pt_livraison):
        messagebox.showerror("Erreur", "Point de départ et/ou Points de livraison incorrects.")
        return None, None

    # Initialisation des solutions optimales
    chemin_optimal = None
    cout_optimal = float('inf')

    # Générer toutes les permutations possibles des nœuds de livraison
    permutations = itertools.permutations(ptLivraison)

    # Pour chaque permutation, trouver le chemin optimal entre le point de départ et les points de livraison
    for perm in permutations:
        chemin_partiel = [pt_depart]
        cout_partiel = 0

        for i in range(len(perm)):
            destination = perm[i]
            chemin, cout = nx.shortest_path(Graphe, source=chemin_partiel[-1], target=destination,
                                            weight='weight'), nx.shortest_path_length(Graphe, source=chemin_partiel[-1],
                                                                                      target=destination,
                                                                                      weight='weight')

            if chemin is not None:
                chemin_partiel += chemin[1:]
                cout_partiel += cout
            else:
                # Pas de chemin possible entre les points de livraison, abandonner cette permutation
                break

        # Ajout du chemin retour entre le dernier point de livraison et le point de départ
        chemin_retour, cout_retour = nx.shortest_path(Graphe, source=chemin_partiel[-1], target=pt_depart,
                                                      weight='weight'), nx.shortest_path_length(Graphe,
                                                                                                source=chemin_partiel[
                                                                                                    -1],
                                                                                                target=pt_depart,
                                                                                                weight='weight')
        chemin_partiel += chemin_retour[1:]
        cout_partiel += cout_retour

        # Mettre à jour la solution optimale si le coût est inférieur
        if cout_partiel < cout_optimal:
            cout_optimal = cout_partiel
            chemin_optimal = chemin_partiel

    return chemin_optimal, cout_optimal

# ------------------------------------------ PARTIE MATPLOTLIB.PYPLOT ------------------------------------------------


cheminfichier = r'C:\Users\jeje9\Documents\copiegraphe.txt'
graph = LectureFichier(cheminfichier)


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

# Modélisation du graphe
nx.draw(graph, positions, with_labels=True, node_size=700, node_color="skyblue", font_size=8, font_color="black",
        font_weight="bold", edge_color="gray", linewidths=1, font_family="sans-serif",
        connectionstyle='arc3,rad=0.1', arrowsize=20)

# Affichage des poids des arêtes
LabelPoidsArete = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, positions, edge_labels=LabelPoidsArete)

# Affichage du graphe
# plt.show(block=False)
# plt.pause(0.1)


# ---------------------------------------------- PARTIE TKINTER ------------------------------------------------------

class Application(tk.Tk):
    def __init__(self, graphE):
        super().__init__()

        self.title("GRAPHE ROUTES DE GUADELOUPE")

        # Création des variables
        self.graph = graphE
        self.cheminOptimal = None
        self.coutOptimal = None
        self.pointsLivraison = []
        self.frame_result = None
        self.label_chemin = None
        self.label_cout = None
        self.points_livraison_entry = None
        self.point_depart = None

        # Création des onglets
        self.tab_control = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Graphe originel')
        self.tab_control.add(self.tab2, text='Voyageur de commerce')
        self.tab_control.add(self.tab3, text='Résultat')

        self.tab_control.pack(expand=1, fill='both')

        self.Onglet_Voyageur_Commerce(self.tab2)
        self.Onglet_Graphe_Originel(self.tab1)
        self.Onglet_Resultat(self.tab3)

    def Onglet_Graphe_Originel(self, tab):
        # Affichage du graphe sur le premier onglet
        figure, ax = plt.subplots(figsize=(10, 6))
        pos = positions

        # Affichage des arêtes avec les coûts
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))
        nx.draw(self.graph, pos, with_labels=True, connectionstyle='arc3,rad=0.1', edgelist=self.graph.edges(),
                arrowsize=20, ax=ax, node_size=800, node_color='skyblue')

        canvas = FigureCanvasTkAgg(figure, master=tab)
        canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew", padx=10, pady=10)
        canvas.draw()

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)

    def Onglet_Voyageur_Commerce(self, tab):
        # Ajout du label en haut, au milieu et en dehors du cadre central
        lbl_liste_noeuds = ttk.Label(tab,
                                     text="Voici la liste des nœuds du graphe: {}".format(list(self.graph.nodes())),
                                     font=("Helvetica", 15, "bold"), foreground="black", wraplength=999)
        lbl_liste_noeuds.grid(row=0, column=0, pady=1)

        # Création d'un frame central pour centrer les labels et zones de texte
        frame_central = ttk.Frame(tab, borderwidth=3, relief="solid", style="Custom.TFrame")
        frame_central.grid(row=1, column=0, pady=1)  # Utilisation de grid pour centrer
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#343541")

        # Ajout du label "VOYAGEUR DE COMMERCE" avec un fond coloré
        lbl_titre = ttk.Label(frame_central, text="VOYAGEUR DE COMMERCE", font=("Helvetica", 14, "bold"),
                              background="#f8f7f7")
        lbl_titre.grid(row=0, column=0, columnspan=2, pady=10)

        # Ajout du label "Point de départ"
        lbl_depart = ttk.Label(frame_central, text="Point de départ:", font="bold")
        lbl_depart.grid(row=1, column=0, padx=10, pady=10)

        # Ajoute la liaison de la touche Entrée à la fonction calculer
        self.bind('<Return>', lambda event=None: self.calculer())

        # Ajout de la zone de texte pour le point de départ
        self.point_depart = ttk.Entry(frame_central)
        self.point_depart.grid(row=1, column=1, padx=10, pady=10)

        # Ajout du label "Points de livraison"
        lbl_livraison = ttk.Label(frame_central, text="Points de livraison (séparés par des espaces):", font="bold")
        lbl_livraison.grid(row=2, column=0, padx=10, pady=10)

        # Ajout de la zone de texte pour les points de livraison
        self.points_livraison_entry = ttk.Entry(frame_central)
        self.points_livraison_entry.grid(row=2, column=1, padx=10, pady=10)

        style.configure("Bold.TButton", font=("TkDefaultFont", 12, "bold"))
        # Ajout du bouton "Lancer"
        btn_calculer = ttk.Button(frame_central, text="Lancer", command=self.calculer, style="Bold.TButton")
        btn_calculer.grid(row=3, column=0, columnspan=2, pady=10)

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=0)
        tab.rowconfigure(1, weight=1)

    def Onglet_Resultat(self, tab):
        # Affichage du résultat sur le troisième onglet

        self.label_cout = ttk.Label(tab, text="", font=("TkDefaultFont", 14, "bold"))
        self.label_cout.grid(column=1, row=0)

        self.label_chemin = ttk.Label(tab, text="", font=("TkDefaultFont", 14, "bold"))
        self.label_chemin.grid(column=1, row=1)

        # Ajout d'une Frame pour afficher le graphe dans le même style que l'onglet "Graphe originel"
        self.frame_result = ttk.Frame(tab)
        self.frame_result.grid(column=0, row=2, columnspan=3)

    def calculer(self):
        # Méthode appeler lors du clic sur le bouton "Lancer", qui fait appel à la fonction "PlusCourtCircuit"
        # Et met à jour le graphe avec les bonnes couleurs dans le 3ᵉ onglet
        pt_depart = self.point_depart.get()

        points_livraison = self.points_livraison_entry.get().split()
        self.cheminOptimal, self.coutOptimal = PlusCourtCircuit(self.graph, pt_depart, points_livraison)
        self.label_cout.config(text=f"Coût optimal: {self.coutOptimal}")

        if self.cheminOptimal is not None and self.coutOptimal is not None:

            # Mise à jour du graphe dans le 3ᵉ onglet avec les couleurs
            figure, ax = plt.subplots(figsize=(15, 9))
            pos = positions
            NoeudCircuitOptimal = set(self.cheminOptimal)
            chemin_str = ", ".join(self.cheminOptimal)
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'))

            couleurs_noeuds = [
                'red' if node == pt_depart else 'green' if node in NoeudCircuitOptimal else 'skyblue' for
                node in self.graph.nodes()]

            nx.draw(self.graph, pos, with_labels=True, connectionstyle='arc3,rad=0.1', edgelist=self.graph.edges(),
                    arrowsize=20, ax=ax, node_size=800, node_color=couleurs_noeuds)

            # Vérifier s'il y a déjà un widget dans frame_result et le détruire
            if self.frame_result.winfo_children():
                for widget in self.frame_result.winfo_children():
                    widget.destroy()

            # Création d'un canvas pour encapsuler le graphe
            canvas = FigureCanvasTkAgg(figure, master=self.frame_result)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)

            # Ajout d'une barre de défilement verticale pour le canvas
            scrollbar = ttk.Scrollbar(self.frame_result, orient="vertical", command=canvas_widget.yview)
            scrollbar.grid(column=1, row=0, sticky="ns")

            # Configuration du canvas pour la barre de défilement
            canvas_widget.config(yscrollcommand=scrollbar.set)

            # Configuration de la grille pour la gestion de la taille
            self.frame_result.columnconfigure(0, weight=1)
            self.frame_result.rowconfigure(0, weight=1)
            self.label_chemin.config(text=f"Chemin optimal: {chemin_str}")

        else:
            self.label_chemin.config(text="Chemin optimal: Aucun chemin trouvé")
            self.label_cout.config(text="Coût optimal: Aucun coût trouvé")
            for widget in self.frame_result.winfo_children():
                widget.destroy()


chemin_fichier = r'C:\Users\jeje9\Documents\copiegraphe.txt'
graphe = LectureFichier(chemin_fichier)

app = Application(graphe)
app.mainloop()

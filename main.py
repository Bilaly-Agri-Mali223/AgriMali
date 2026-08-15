import json

from datetime import datetime

import tkinter as tk

from tkinter import ttk, messagebox

DATA_FILE = "fermes.json"

class AgriMaliApp:

    def __init__(self, root):

        self.root = root

        self.root.title("🌱 AgriMali - Smart Farm Manager")

        self.root.geometry("1050x700")

        self.root.minsize(900, 600)

        self.fermes = []

        self.charger_donnees()

        self.creer_style()

        self.creer_interface()

        self.actualiser_tableau()

        self.actualiser_statistiques()

    # -------------------------

    # DONNÉES

    # -------------------------

    def charger_donnees(self):

        try:

            with open(DATA_FILE, "r", encoding="utf-8") as fichier:

                self.fermes = json.load(fichier)

        except (FileNotFoundError, json.JSONDecodeError):

            self.fermes = []

    def sauvegarder_donnees(self):

        with open(DATA_FILE, "w", encoding="utf-8") as fichier:

            json.dump(self.fermes, fichier, indent=4, ensure_ascii=False)

    # -------------------------

    # STYLE

    # -------------------------

    def creer_style(self):

        style = ttk.Style()

        try:

            style.theme_use("clam")

        except tk.TclError:

            pass

        style.configure(

            "Title.TLabel",

            font=("Arial", 24, "bold")

        )

        style.configure(

            "Subtitle.TLabel",

            font=("Arial", 11)

        )

        style.configure(

            "Treeview",

            rowheight=32,

            font=("Arial", 10)

        )

        style.configure(

            "Treeview.Heading",

            font=("Arial", 10, "bold")

        )

        style.configure(

            "Action.TButton",

            font=("Arial", 10, "bold"),

            padding=8

        )

    # -------------------------

    # INTERFACE

    # -------------------------

    def creer_interface(self):

        # En-tête

        header = ttk.Frame(self.root, padding=15)

        header.pack(fill="x")

        ttk.Label(

            header,

            text="🌱 AGRIMALI",

            style="Title.TLabel"

        ).pack(anchor="w")

        ttk.Label(

            header,

            text="Smart Farm Management System",

            style="Subtitle.TLabel"

        ).pack(anchor="w")

        # Statistiques

        stats_frame = ttk.Frame(self.root, padding=(15, 5))

        stats_frame.pack(fill="x")

        self.total_label = ttk.Label(

            stats_frame,

            text="🏠 Fermes : 0",

            font=("Arial", 12, "bold")

        )

        self.total_label.pack(side="left", padx=10)

        self.villes_label = ttk.Label(

            stats_frame,

            text="📍 Villes : 0",

            font=("Arial", 12, "bold")

        )

        self.villes_label.pack(side="left", padx=10)

        self.cultures_label = ttk.Label(

            stats_frame,

            text="🌾 Cultures : 0",

            font=("Arial", 12, "bold")

        )

        self.cultures_label.pack(side="left", padx=10)

        # Formulaire

        form = ttk.LabelFrame(

            self.root,

            text="Informations de la ferme",

            padding=15

        )

        form.pack(fill="x", padx=15, pady=10)

        ttk.Label(form, text="Nom de la ferme").grid(

            row=0, column=0, padx=5, pady=5, sticky="w"

        )

        self.nom_entry = ttk.Entry(form, width=25)

        self.nom_entry.grid(

            row=0, column=1, padx=5, pady=5

        )

        ttk.Label(form, text="Culture").grid(

            row=0, column=2, padx=5, pady=5, sticky="w"

        )

        self.culture_entry = ttk.Entry(form, width=25)

        self.culture_entry.grid(

            row=0, column=3, padx=5, pady=5

        )

        ttk.Label(form, text="Ville").grid(

            row=1, column=0, padx=5, pady=5, sticky="w"

        )

        self.ville_entry = ttk.Entry(form, width=25)

        self.ville_entry.grid(

            row=1, column=1, padx=5, pady=5

        )

        ttk.Label(form, text="Téléphone").grid(

            row=1, column=2, padx=5, pady=5, sticky="w"

        )

        self.telephone_entry = ttk.Entry(form, width=25)

        self.telephone_entry.grid(

            row=1, column=3, padx=5, pady=5

        )

        # Boutons

        buttons = ttk.Frame(form)

        buttons.grid(

            row=2,

            column=0,

            columnspan=4,

            pady=10

        )

        ttk.Button(

            buttons,

            text="➕ Ajouter",

            style="Action.TButton",

            command=self.ajouter_ferme

        ).pack(side="left", padx=5)

        ttk.Button(

            buttons,

            text="✏️ Modifier",

            style="Action.TButton",

            command=self.modifier_ferme

        ).pack(side="left", padx=5)

        ttk.Button(

            buttons,

            text="🗑️ Supprimer",

            style="Action.TButton",

            command=self.supprimer_ferme

        ).pack(side="left", padx=5)

        ttk.Button(

            buttons,

            text="🧹 Vider",

            style="Action.TButton",

            command=self.vider_formulaire

        ).pack(side="left", padx=5)

        # Recherche

        search_frame = ttk.Frame(

            self.root,

            padding=(15, 5)

        )

        search_frame.pack(fill="x")

        ttk.Label(

            search_frame,

            text="🔎 Rechercher :"

        ).pack(side="left", padx=5)

        self.recherche_entry = ttk.Entry(

            search_frame,

            width=40

        )

        self.recherche_entry.pack(

            side="left",

            padx=5

        )

        self.recherche_entry.bind(

            "<KeyRelease>",

            self.rechercher

        )

        ttk.Button(

            search_frame,

            text="Afficher tout",

            command=self.afficher_tout

        ).pack(side="left", padx=5)

        # Tableau

        table_frame = ttk.Frame(

            self.root,

            padding=15

        )

        table_frame.pack(

            fill="both",

            expand=True

        )

        colonnes = (

            "nom",

            "culture",

            "ville",

            "telephone",

            "date"

        )

        self.tableau = ttk.Treeview(

            table_frame,

            columns=colonnes,

            show="headings"

        )

        self.tableau.heading(

            "nom",

            text="Ferme"

        )

        self.tableau.heading(

            "culture",

            text="Culture"

        )

        self.tableau.heading(

            "ville",

            text="Ville"

        )

        self.tableau.heading(

            "telephone",

            text="Téléphone"

        )

        self.tableau.heading(

            "date",

            text="Date d'ajout"

        )

        self.tableau.column(

            "nom",

            width=200

        )

        self.tableau.column(

            "culture",

            width=150

        )

        self.tableau.column(

            "ville",

            width=150

        )

        self.tableau.column(

            "telephone",

            width=150

        )

        self.tableau.column(

            "date",

            width=150

        )

        scrollbar = ttk.Scrollbar(

            table_frame,

            orient="vertical",

            command=self.tableau.yview

        )

        self.tableau.configure(

            yscrollcommand=scrollbar.set

        )

        self.tableau.pack(

            side="left",

            fill="both",

            expand=True

        )

        scrollbar.pack(

            side="right",

            fill="y"

        )

        self.tableau.bind(

            "<<TreeviewSelect>>",

            self.selectionner_ferme

        )

        # Message

        self.message_label = ttk.Label(

            self.root,

            text="Bienvenue dans AgriMali 🌱",

            font=("Arial", 10)

        )

        self.message_label.pack(

            pady=8

        )

    # -------------------------

    # AJOUTER

    # -------------------------

    def ajouter_ferme(self):

        nom = self.nom_entry.get().strip()

        culture = self.culture_entry.get().strip()

        ville = self.ville_entry.get().strip()

        telephone = self.telephone_entry.get().strip()

        if not nom or not culture or not ville or not telephone:

            messagebox.showwarning(

                "Champs obligatoires",

                "Veuillez remplir tous les champs."

            )

            return

        ferme = {

            "nom": nom,

            "culture": culture,

            "ville": ville,

            "telephone": telephone,

            "date": datetime.now().strftime("%d/%m/%Y")

        }

        self.fermes.append(ferme)

        self.sauvegarder_donnees()

        self.actualiser_tableau()

        self.actualiser_statistiques()

        self.vider_formulaire()

        self.message_label.config(

            text="✅ Ferme ajoutée avec succès."

        )

    # -------------------------

    # MODIFIER

    # -------------------------

    def modifier_ferme(self):

        selection = self.tableau.selection()

        if not selection:

            messagebox.showwarning(

                "Aucune sélection",

                "Sélectionnez une ferme à modifier."

            )

            return

        index = int(selection[0])

        nom = self.nom_entry.get().strip()

        culture = self.culture_entry.get().strip()

        ville = self.ville_entry.get().strip()

        telephone = self.telephone_entry.get().strip()

        if not nom or not culture or not ville or not telephone:

            messagebox.showwarning(

                "Champs obligatoires",

                "Veuillez remplir tous les champs."

            )

            return

        self.fermes[index]["nom"] = nom

        self.fermes[index]["culture"] = culture

        self.fermes[index]["ville"] = ville

        self.fermes[index]["telephone"] = telephone

        self.sauvegarder_donnees()

        self.actualiser_tableau()

        self.actualiser_statistiques()

        self.vider_formulaire()

        self.message_label.config(

            text="✏️ Ferme modifiée avec succès."

        )

    # -------------------------

    # SUPPRIMER

    # -------------------------

    def supprimer_ferme(self):

        selection = self.tableau.selection()

        if not selection:

            messagebox.showwarning(

                "Aucune sélection",

                "Sélectionnez une ferme à supprimer."

            )

            return

        index = int(selection[0])

        confirmation = messagebox.askyesno(

            "Confirmation",

            "Voulez-vous vraiment supprimer cette ferme ?"

        )

        if not confirmation:

            return

        self.fermes.pop(index)

        self.sauvegarder_donnees()

        self.actualiser_tableau()

        self.actualiser_statistiques()

        self.vider_formulaire()

        self.message_label.config(

            text="🗑️ Ferme supprimée."

        )

    # -------------------------

    # RECHERCHE

    # -------------------------

    def rechercher(self, event=None):

        mot = self.recherche_entry.get().lower().strip()

        self.tableau.delete(

            *self.tableau.get_children()

        )

        for index, ferme in enumerate(self.fermes):

            texte = (

                ferme["nom"] + " "

                + ferme["culture"] + " "

                + ferme["ville"] + " "

                + ferme["telephone"]

            ).lower()

            if mot in texte:

                self.tableau.insert(

                    "",

                    "end",

                    iid=str(index),

                    values=(

                        ferme["nom"],

                        ferme["culture"],

                        ferme["ville"],

                        ferme["telephone"],

                        ferme["date"]

                    )

                )

    # -------------------------

    # AFFICHER

    # -------------------------

    def afficher_tout(self):

        self.recherche_entry.delete(0, tk.END)

        self.actualiser_tableau()

    def actualiser_tableau(self):

        self.tableau.delete(

            *self.tableau.get_children()

        )

        for index, ferme in enumerate(self.fermes):

            self.tableau.insert(

                "",

                "end",

                iid=str(index),

                values=(

                    ferme["nom"],

                    ferme["culture"],

                    ferme["ville"],

                    ferme["telephone"],

                    ferme["date"]

                )

            )

    # -------------------------

    # SÉLECTION

    # -------------------------

    def selectionner_ferme(self, event=None):

        selection = self.tableau.selection()

        if not selection:

            return

        index = int(selection[0])

        if index >= len(self.fermes):

            return

        ferme = self.fermes[index]

        self.nom_entry.delete(0, tk.END)

        self.nom_entry.insert(0, ferme["nom"])

        self.culture_entry.delete(0, tk.END)

        self.culture_entry.insert(0, ferme["culture"])

        self.ville_entry.delete(0, tk.END)

        self.ville_entry.insert(0, ferme["ville"])

        self.telephone_entry.delete(0, tk.END)

        self.telephone_entry.insert(

            0,

            ferme["telephone"]

        )

    # -------------------------

    # VIDER

    # -------------------------

    def vider_formulaire(self):

        self.nom_entry.delete(0, tk.END)

        self.culture_entry.delete(0, tk.END)

        self.ville_entry.delete(0, tk.END)

        self.telephone_entry.delete(0, tk.END)

        for item in self.tableau.selection():

            self.tableau.selection_remove(item)

    # -------------------------

    # STATISTIQUES

    # -------------------------

    def actualiser_statistiques(self):

        total = len(self.fermes)

        villes = len({

            ferme["ville"].lower()

            for ferme in self.fermes

            if ferme.get("ville")

        })

        cultures = len({

            ferme["culture"].lower()

            for ferme in self.fermes

            if ferme.get("culture")

        })

        self.total_label.config(

            text=f"🏠 Fermes : {total}"

        )

        self.villes_label.config(

            text=f"📍 Villes : {villes}"

        )

        self.cultures_label.config(

            text=f"🌾 Cultures : {cultures}"

        )

def main():

    root = tk.Tk()

    application = AgriMaliApp(root)

    root.mainloop()

if __name__ == "__main__":

    main()

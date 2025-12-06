# Importation
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import messagebox
from datetime import date
import hashlib

                          # ---------------------------------------------
                            #Projet – Programmation – Compétence 00Q2-00Q6

                                  # Djinadou Oladokun Mahanfouz
                          # ---------------------------------------------

# -------------------------
# 1- Modèle (Classes)
# -------------------------

# Classe de base pour toute personne dans le système
class Personne:
    def __init__(self, nom, prenom, sexe):
        # Attributs communs à toutes les personnes
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe

    # Affiche le nom complet de la personne pour un affichage lisible
    def __repr__(self):
        return f"{self.prenom} {self.nom}"

# CarteCredit
class CarteCredit:
    def __init__(self, numero, date_expiration, code_secret):
        self.numero = numero
        self.date_expiration = date_expiration
        self.code_secret = code_secret

# Client
class Client(Personne):
    def __init__(self, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        super().__init__(nom, prenom, sexe) # récupères automatiquement les attributs de Personne
        self.date_inscription = date_inscription
        self.courriel = courriel
        self.mot_de_passe = mot_de_passe
        self.cartes_credit = []  # Possibilité d'enregistrer plusieurs cartes bancaires.

    # Pensez à la sécurité (password = 8 caractères min, encryption)
    def check_mot_de_passe(self, raw_password):
        return hashlib.sha256(raw_password.encode('utf-8')).hexdigest() == self.mot_de_passe

# Acteur
class Acteur(Personne):
    def __init__(self, nom, prenom, sexe, nom_personnage, debut_emploi, fin_emploi, cachet):
        super().__init__(nom, prenom, sexe)  # récupères automatiquement les attributs de Personne
        self.nom_personnage = nom_personnage
        self.debut_emploi = debut_emploi
        self.fin_emploi = fin_emploi
        self.cachet = cachet

# # Hérite de Personne et représente un employé du système
class Employe(Personne):
    def __init__(self, nom, prenom, sexe, date_embauche, code_utilisateur, mot_de_passe, type_acces):
        super().__init__(nom, prenom, sexe)  # récupères automatiquement les attributs de Personne
        self.date_embauche = date_embauche
        self.code_utilisateur = code_utilisateur
        self.mot_de_passe = mot_de_passe
        self.type_acces = type_acces  # 'total'(droit de modification) ou 'lecture'(lecture seule)

    # Pensez à la sécurité (password = 8 caractères min, encryption)
    def check_mot_de_passe(self, raw_password):
        return hashlib.sha256(raw_password.encode('utf-8')).hexdigest() == self.mot_de_passe

# Categorie
class Categorie:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description

    # Affiche simplement le nom de la catégorie
    def __repr__(self):
        return self.nom

# Film
class Film:
    def __init__(self, nom, duree, description):
        self.nom = nom
        self.duree = duree
        self.description = description
        self.categories = []   # Un film peut avoir plus d’une catégorie
        self.acteurs = []      # Un acteur peut avoir joué dans plusieurs films

    # Retourne une représentation lisible du film pour affichage
    def __repr__(self):
        cats = ','.join([c.nom for c in self.categories])
        return f"{self.nom} ({self.duree}min) [{cats}]"



# -------------------------
# 2- Gestion des utilisateurs
# -------------------------
class Gestionnaire:
    def __init__(self):
        # mots de passe hachés pour démonstration de sécurité (sha256)
        def h(p): return hashlib.sha256(p.encode('utf-8')).hexdigest()

        # Création des employés (code_utilisateur, mot_de_passe)
        self.employes = [
            Employe('Djinadou','Jean','M','2020-01-01','E001', h('12345678'), 'total'),
            Employe('Gagnon','Marie','F','2021-05-10','E002', h('qwertyui'), 'lecture')
        ]

        # quelques clients
        self.clients = [
            Client('Pele','Luc','M', '2022-02-02', 'luc@gmail.com', h('87654321')),
            Client('Guy','Ola','F', '2023-03-03', 'ola@example.com', h('azertyui'))
        ]

        # Création catégories et films
        c1 = Categorie('Comédie','Films drôles')
        c2 = Categorie('Action','Films action')
        f1 = Film('Le Grand Rire', 95, 'Une comédie familial')
        f1.categories = [c1]
        f2 = Film('Choc et Fracas', 120, 'Action non-stop')
        f2.categories = [c2]
        self.films = [f1,f2]

    # Fonction verifier_connexion
    #  Retourne l'objet Employe si OK, sinon None
    def verifier_connexion(self, code, raw_password):
        for e in self.employes:
            if e.code_utilisateur == code and e.check_mot_de_passe(raw_password):
                return e
        return None


    # -------------------------
    # CRUD client (CRUD = Create, Read, Update, Delete)
    # -------------------------
    #Ajouter client
    def ajouter_client(self, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        # Vérifie la longueur du mot de passe
        if len(mot_de_passe) < 8:
            raise ValueError('Le Mot de passe doit avoir au moins 8 caractères')
        # Vérifie si un client n’a pas déjà ce courriel
        if any(c.courriel.lower() == courriel.lower() for c in self.clients):
            raise ValueError('Courriel déjà utilisé')

        # Hash du mot de passe
        h = hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()
        new = Client(nom, prenom, sexe, date_inscription, courriel, h)
        # Pour que le programme puisse gérer plusieurs clients :
        self.clients.append(new)
        return new

    # Modifier client
    def modifier_client(self, client_obj, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        # Vérifie la longueur du mot de passe
        if len(mot_de_passe) < 8:
            raise ValueError('Mot de passe doit être au moins 8 caractères')
        # Vérifier que personne d'autre n'utilise le même courriel
        for c in self.clients:
            if c is not client_obj and c.courriel.lower() == courriel.lower():
                raise ValueError('Courriel déjà utilisé par un autre client')
        # Hash du mot de passe
        h = hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()

        # Met à jour toutes les informations de l’objet client_obj
        client_obj.nom = nom
        client_obj.prenom = prenom
        client_obj.sexe = sexe
        client_obj.date_inscription = date_inscription
        client_obj.courriel = courriel
        client_obj.mot_de_passe = h
        return client_obj  #Retourne l’objet modifié

    # Supprimer client
    # Retourne True si la suppression s’est faite, Sinon retourne False
    def supprimer_client(self, client_obj):
        # Vérifie si le client est dans la liste
        if client_obj in self.clients:
            self.clients.remove(client_obj)
            return True
        return False


# ------------------------------------------
#  3- Fenêtre principale (Page de connection)
# ------------------------------------------
class PageDeConnection:
    def __init__(self, fenetre):
        # Initialise la fenêtre de connexion principale.
        self.fenetre = fenetre
        self.fenetre.title('Connexion Employé')
        self.fenetre.geometry('360x140')
        self.gestion = Gestionnaire()

        # Création des labels pour le formulaire
        tk.Label(fenetre, text='Code utilisateur:').grid(row=0, column=0, padx=8, pady=6)
        tk.Label(fenetre, text='Mot de passe:').grid(row=1, column=0, padx=8, pady=6)

        # Champs de saisie pour code utilisateur et mot de passe
        self.code_utilisateur_entry = tk.Entry(fenetre)
        self.code_utilisateur_entry.grid(row=0, column=1, padx=8, pady=6)
        self.mot_de_passe_entry = tk.Entry(fenetre, show='*')
        self.mot_de_passe_entry.grid(row=1, column=1, padx=8, pady=6)

        # Bouton pour lancer la connexion
        tk.Button(fenetre, text='Connexion', command=self.login).grid(row=2, column=1, sticky='e', padx=8, pady=6)

    def login(self):
        # Récupération et nettoyage des entrées
        code = self.code_utilisateur_entry.get().strip()  # Récupère le Code utilisateur entré et Enlève les espaces avant et après
        password = self.mot_de_passe_entry.get().strip()  # Récupère le mot de passe entré et Enlève les espaces avant et après
        try:
            # Vérifie la connexion via le gestionnaire
            employe = self.gestion.verifier_connexion(code, password)
            if employe:
                # Connexion réussie : message de bienvenue
                messagebox.showinfo('Succès', f'Bienvenue {employe.nom} ({employe.type_acces})')
                self.fenetre.withdraw()  # Masque la fenêtre de connexion
                MainWindow(self.fenetre, self.gestion, employe)  # Ouvre la fenêtre principale
            else:
                # Code ou mot de passe incorrect
                messagebox.showerror('Erreur', 'Code ou mot de passe incorrect.')
        except Exception as e:
            # Gestion des exceptions inattendues
            messagebox.showerror('Erreur', str(e))



# ------------------------------------------
#  4- Fenêtre Gestion clients & films
# ------------------------------------------
class MainWindow:
    def __init__(self, root, gestion, employe):
        self.root = root
        self.gestion = gestion
        self.employe = employe
        self.win = tk.Toplevel(root)
        self.win.title('Plateforme - Gestion clients & films')
        self.win.geometry('1200x450')

        ### Menu "Compte"
        menubar = tk.Menu(self.win)
        account_menu = tk.Menu(menubar, tearoff=0)
        # Se déconnecter → ferme la fenêtre et retourne au login.
        account_menu.add_command(label='Se déconnecter', command=self.logout)
        account_menu.add_separator()
        # Quitter → ferme complètement l’application.
        account_menu.add_command(label='Quitter', command=self.quit_app)
        menubar.add_cascade(label='Compte', menu=account_menu)
        self.win.config(menu=menubar)

        ### Cadre Clients
        cframe = tk.LabelFrame(self.win, text='Clients')
        cframe.pack(side='left', fill='y', padx=8, pady=8)

        # Tableau (Treeview) affichant les clients
        cols = ('nom','prenom','courriel')
        self.client_tree = ttk.Treeview(cframe, columns=cols, show='headings', height=15)
        # Ligne simple qui met la première lettre en majuscule.
        for c in cols:
            self.client_tree.heading(c, text=c.title())
        self.client_tree.pack(side='top', padx=4, pady=4)

        ### Les Boutons client (créer, modifier, supprimer)
        btn_frame = tk.Frame(cframe)
        btn_frame.pack(side='top', pady=6)
        # On ajoute trois(3) boutons : créer, modifier, supprimer.
        self.add_btn = tk.Button(btn_frame, text='Créer client', command=self.create_client)
        self.edit_btn = tk.Button(btn_frame, text='Modifier client', command=self.edit_client)
        self.del_btn = tk.Button(btn_frame, text='Supprimer client', command=self.delete_client)
        self.add_btn.grid(row=0,column=0,padx=4)
        self.edit_btn.grid(row=0,column=1,padx=4)
        self.del_btn.grid(row=0,column=2,padx=4)

        ### Gestion des films
        f_frame = tk.LabelFrame(self.win, text='Films')
        f_frame.pack(side='right', fill='both', expand=True, padx=8, pady=8)
        # Tableau des films
        f_cols = ('nom','durée','categories')
        self.film_tree = ttk.Treeview(f_frame, columns=f_cols, show='headings', height=10)
        for c in f_cols:
            self.film_tree.heading(c, text=c.title())
        self.film_tree.pack(fill='both', expand=True, padx=4, pady=4)
        # Quand la souris bouge au-dessus de la liste, on appelle _on_film_motion.
        self.film_tree.bind('<Motion>', self._on_film_motion)

        # initialisé
        self._refresh_clients()
        self._refresh_films()

        # Si l’employé n’a que le droit lecture, il ne peut ni créer, ni modifier, ni supprimer un client.
        if self.employe.type_acces == 'lecture':
            self.add_btn.config(state='disabled')
            self.edit_btn.config(state='disabled')
            self.del_btn.config(state='disabled')

    # Actualise l'affichage des clients dans le tableau
    def _refresh_clients(self):
        # On vide le tableau existant pour éviter les doublons
        for i in self.client_tree.get_children():
            self.client_tree.delete(i)
        # Remet tous les clients depuis gestion clients
        for idx, c in enumerate(self.gestion.clients):
            self.client_tree.insert('', 'end', iid=str(idx), values=(c.nom, c.prenom, c.courriel))

    # Actualise l'affichage des films dans le tableau
    def _refresh_films(self):
        # On vide le tableau des films pour le réactualiser proprement
        for i in self.film_tree.get_children():
            self.film_tree.delete(i)
        # transforme une liste de catégories en une seule chaîne.
        for idx, f in enumerate(self.gestion.films):
            cats = ', '.join([cat.nom for cat in f.categories])
            self.film_tree.insert('', 'end', iid=str(idx), values=(f.nom, f.duree, cats))

    # Détecte la ligne survolée avec la souris dans le tableau des films
    def _on_film_motion(self, event):
        # Cherche l'identifiant (iid) de la ligne sous la souris
        item = self.film_tree.identify_row(event.y)
        if item:
            # Récupère l'objet Film correspondant à cette ligne
            film = self.gestion.films[int(item)]
            # Récupère la liste des acteurs si elle existe, sinon liste vide
            # S'il n'y a aucun acteur : affiche "Aucun acteur renseigné"
            actors = ', '.join([repr(a) for a in getattr(film, 'acteurs', [])]) or 'Aucun acteur renseigné'
            self.win.title(f'Plateforme - Gestion clients & films - Acteurs: {actors}')

    # Ouvre une petite fenêtre de création.
    def create_client(self):
        ClientCreateWindow(self.win, self.gestion, on_success=self._refresh_clients)

    # Vérifie si un élément est sélectionné, Récupère l’objet client correspondant et Ouvre la fenêtre d’édition
    def edit_client(self):
        # Récupère la sélection dans le tableau
        sel = self.client_tree.selection()
        # Aucun élément sélectionné → message d'avertissement
        if not sel:
            messagebox.showwarning('Attention', 'Sélectionnez un client à modifier.')
            return
        # Chaque entrée du Treeview utilise son index dans la liste comme iid
        idx = int(sel[0])
        # Récupère l'objet client à partir de l'index
        client_obj = self.gestion.clients[idx]
        # Ouvre la fenêtre d’édition avec l'objet existant
        ClientEditWindow(self.win, self.gestion, client_obj, on_success=self._refresh_clients)

    # Vérifie si une ligne est sélectionnée, Ouvre une boîte de confirmation et Supprime
    def delete_client(self):
        sel = self.client_tree.selection()
        # Si aucune ligne sélectionnée → avertissement
        if not sel:
            messagebox.showwarning('Attention', 'Sélectionnez un client à supprimer.')
            return
        idx = int(sel[0])
        client_obj = self.gestion.clients[idx]
        # Boîte de confirmation → retourne True ou False
        if confirm_delete(self.win, f'Voulez-vous supprimer {client_obj.prenom} {client_obj.nom} ?'):
            try:
                self.gestion.supprimer_client(client_obj)
                messagebox.showinfo('Succès', 'Client supprimé.')
                self._refresh_clients()
            except Exception as e:
                # En cas d'erreur inattendue (base de données, logique…)
                messagebox.showerror('Erreur', str(e))

    # Ferme cette fenêtre principale et réaffiche la fenêtre login (fenetre)
    def logout(self):
        # Ferme la fenêtre principale
        self.win.destroy()
        # Réaffiche la fenêtre de login cachée
        self.root.deiconify()

    # Ferme toutes les fenêtres → quitte l’application.
    def quit_app(self):
        # Ferme la fenêtre principale
        self.win.destroy()
        # Ferme la fenêtre de login → application terminée
        self.root.destroy()



# ------------------------
# 5- Fenêtre Création du client
# ------------------------------------------
class ClientCreateWindow:
    def __init__(self, parent, gestion, on_success=None):
        # Création d'une nouvelle petite fenêtre (popup)
        self.top = tk.Toplevel(parent)
        self.top.title('Créer Client')
        self.gestion = gestion
        self.on_success = on_success

        # Liste des champs du formulaire
        labels = ['Nom','Prénom','Sexe','Date inscription (YYYY-MM-DD)','Courriel','Mot de passe']
        # Dictionnaire qui stockera chaque Entry pour faciliter la récupération
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(self.top, text=lab+':').grid(row=i, column=0, sticky='e', padx=6, pady=4)
            ent = tk.Entry(self.top, width=30, show='*' if 'Mot de passe' in lab else None)
            ent.grid(row=i, column=1, padx=6, pady=4)
            self.entries[lab] = ent

        # Bouton pour valider le formulaire
        tk.Button(self.top, text='Valider', command=self.create).grid(row=len(labels), column=1, sticky='e', padx=6, pady=8)

    def create(self):
        try:
            # Récupération des valeurs
            nom = self.entries['Nom'].get().strip()
            prenom = self.entries['Prénom'].get().strip()
            sexe = self.entries['Sexe'].get().strip()
            date_ins = self.entries['Date inscription (YYYY-MM-DD)'].get().strip() or date.today().isoformat()
            courriel = self.entries['Courriel'].get().strip()
            pwd = self.entries['Mot de passe'].get()

            # validations simples
            if not (nom and prenom and courriel and pwd):
                raise ValueError('Tous les champs obligatoires doivent être remplis.')
            if '@' not in courriel or '.' not in courriel:
                raise ValueError('Courriel invalide.')
            # delegate to gestionnaire (will raise on invalid)
            self.gestion.ajouter_client(nom, prenom, sexe, date_ins, courriel, pwd)
            messagebox.showinfo('Succès', 'Client créé.')
            # Si une fonction de rafraîchissement a été fournie
            if self.on_success:
                self.on_success()
            # Fermeture de la fenêtre après création
            self.top.destroy()
        except Exception as e:
            # Affichage d'une erreur en cas de problème
            messagebox.showerror('Erreur', str(e))



# ------------------------
# 6- Fenêtre Modifier client
# ------------------------------------------
class ClientEditWindow:
    def __init__(self, parent, gestion, client_obj, on_success=None):
        # Nouvelle fenêtre pour l'édition
        self.top = tk.Toplevel(parent)
        self.top.title('Modifier Client')
        self.gestion = gestion
        self.client = client_obj
        self.on_success = on_success

        # Liste des champs du formulaire
        labels = ['Nom','Prénom','Sexe','Date inscription (YYYY-MM-DD)','Courriel','Mot de passe']
        self.entries = {}
        # Valeurs initiales (déjà existantes)
        values = [client_obj.nom, client_obj.prenom, client_obj.sexe, client_obj.date_inscription, client_obj.courriel, '']

        # Construction du formulaire
        for i, (lab, val) in enumerate(zip(labels, values)):
            tk.Label(self.top, text=lab+':').grid(row=i, column=0, sticky='e', padx=6, pady=4)
            ent = tk.Entry(self.top, width=30, show='*' if 'Mot de passe' in lab else None)
            ent.insert(0, val)
            ent.grid(row=i, column=1, padx=6, pady=4)
            self.entries[lab] = ent

        # Bouton pour enregistrer les modifications
        tk.Button(self.top, text='Enregistrer', command=self.save).grid(row=len(labels), column=1, sticky='e', padx=6, pady=8)

    def save(self):
        try:
            # Récupération des nouvelles valeurs
            nom = self.entries['Nom'].get().strip()
            prenom = self.entries['Prénom'].get().strip()
            sexe = self.entries['Sexe'].get().strip()
            date_ins = self.entries['Date inscription (YYYY-MM-DD)'].get().strip()
            courriel = self.entries['Courriel'].get().strip()
            pwd = self.entries['Mot de passe'].get()

            # Validations
            if not (nom and prenom and courriel and pwd):
                raise ValueError('Tous les champs obligatoires doivent être remplis.')
            if '@' not in courriel or '.' not in courriel:
                raise ValueError('Courriel invalide.')

            # Appel au gestionnaire (backend)
            self.gestion.modifier_client(self.client, nom, prenom, sexe, date_ins, courriel, pwd)
            messagebox.showinfo('Succès', 'Client modifié.')
            # Rafraîchissement du tableau principal
            if self.on_success:
                self.on_success()
            self.top.destroy()
        except Exception as e:
            # Affichage d'une erreur en cas de problème
            messagebox.showerror('Erreur', str(e))


# ------------------------
# 7- Confirmation dialogue
# ------------------------------------------
def confirm_delete(parent, message):
    # Affiche une boîte de dialogue Oui / Non
    # Retourne True si l’utilisateur clique sur Oui
    return messagebox.askyesno('Confirmation', message, parent=parent)


# ------------------------
# 8- main.py - point d'entrée
# ------------------------------------------
def main():
    # Création de la fenêtre principale (Tk)
    fenetre = tk.Tk()
    # Affichage de la page de connexion
    app = PageDeConnection(fenetre)
    # Boucle principale Tkinter
    fenetre.mainloop()

# Lancement du programme si exécuté directement
if __name__ == '__main__':
    main()

############################################## FIN ####################################################

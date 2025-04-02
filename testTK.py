"""
Fait par Jules
Fichier principale ou le programme doit être lancer pour la version initial.
"""
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from Biblio import *



def ouvrir_inscription():
    """Fonction pour ouvrir la fenêtre d'inscription
    Fait par Jules
    """
    inscription_window = tk.Toplevel(root)
    inscription_window.title("Créer un compte")
    inscription_window.geometry("700x900")
    
    frame = tk.Frame(inscription_window)
    frame.pack(pady=10)
    
    def valider_inscription():
        pseudo = entry_pseudo.get()
        email = entry_email.get()
        mdp = entry_mdp.get()
        age = entry_age.get()
        taille = entry_taille.get()
        poid = entry_poid.get()
        sex = entry_sex.get()
        objectif = entry_objectif.get()
        activite = entry_activite.get()
        
        if not all([pseudo, email, mdp, age, taille, poid, sex, objectif, activite]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return
        
        try:
            age, taille, poid, sex, objectif, activite = map(int, [age, taille, poid, sex, objectif, activite])
        except ValueError:
            messagebox.showerror("Erreur", "Les valeurs numériques sont invalides.")
            return
        
        id_utilisateur = creer_compte(pseudo, email, mdp, age, taille, poid, sex, objectif, activite)
        if id_utilisateur == -1:
            messagebox.showerror("Erreur", "Pseudo ou email déjà utilisé.")
        else:
            messagebox.showinfo("Succès", "Compte créé avec succès ! Redirection vers la connexion...")
            inscription_window.destroy()
            ouvrir_connexion()
    
    labels = ["Pseudo", "Email", "Mot de passe", "Âge", "Taille (cm)", "Poids (kg)", "Sexe (1=H, 2=F)", "Objectif (1,2,3)", "Niveau d'activité (1-5)"]
    entries = []
    
    for label in labels:
        tk.Label(frame, text=label).pack()
        entry = tk.Entry(frame, show="*" if "Mot de passe" in label else None)
        entry.pack()
        entries.append(entry)
    
    entry_pseudo, entry_email, entry_mdp, entry_age, entry_taille, entry_poid, entry_sex, entry_objectif, entry_activite = entries
    
    tk.Button(frame, text="Créer mon compte", command=valider_inscription).pack(pady=10)
def ouvrir_connexion():
    """Fonction pour ouvrir la fenêtre de connexion
    Fait par Jules
    """
    global pseudo_utilisateur, email_utilisateur
    connexion_window = tk.Toplevel(root)
    connexion_window.title("Connexion")
    connexion_window.geometry("300x200")
    
    frame = tk.Frame(connexion_window)
    frame.pack(pady=10)
    
    tk.Label(frame, text="Pseudo").pack()
    entry_pseudo = tk.Entry(frame)
    entry_pseudo.pack()
    pseudo_utilisateur = entry_pseudo

    tk.Label(frame, text="Email").pack()
    entry_email = tk.Entry(frame)
    entry_email.pack()
    email_utilisateur = entry_email

    tk.Label(frame, text="Mot de passe").pack()
    entry_mdp = tk.Entry(frame, show="*")
    entry_mdp.pack()
    
    def verifier_connexion():
        global pseudo_utilisateur, email_utilisateur
        pseudo = entry_pseudo.get()
        email = entry_email.get()
        mdp = entry_mdp.get()
        pseudo_utilisateur = pseudo
        email_utilisateur = email
        if not all([pseudo, email, mdp]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return
        
        id_utilisateur = get_id_utilisateur(pseudo, email)
        if id_utilisateur and Verif_mdp(mdp, id_utilisateur):
            messagebox.showinfo("Succès", "Connexion réussie !")
            connexion_window.destroy()
            ouvrir_lobby()
        else:
            messagebox.showerror("Erreur", "Pseudo, email ou mot de passe incorrect.")

    tk.Button(frame, text="Se connecter", command=verifier_connexion).pack(pady=10)

    def ouvrir_lobby():
        """Fenêtre affichant les kcal consommées et nécessaires."""
        global pseudo_utilisateur, email_utilisateur

        if not pseudo_utilisateur or not email_utilisateur:
            messagebox.showerror("Erreur", "Utilisateur non reconnu. Veuillez vous reconnecter.")
            return

        id_utilisateur = get_id_utilisateur(pseudo_utilisateur, email_utilisateur)
        
        if id_utilisateur is None:
            messagebox.showerror("Erreur", "Impossible de récupérer les informations utilisateur.")
            return

        infos_utilisateur = get_info_utilisateur(id_utilisateur)

        if infos_utilisateur is None:
            messagebox.showerror("Erreur", "Problème de récupération des données.")
            return
        tu , pu , sex , activiter , obj = get_info_utilisateur(id_utilisateur)
        _, _, liste_macros = Besoin(tu , pu , sex , activiter , obj)
        kcal_total, glucides, proteines, lipides = Convert_Macro_to_tuple(liste_macros)

        # Création de la fenêtre du lobby
        fenetre_macros = tk.Toplevel(root)
        fenetre_macros.title("Suivi des Macros")
        fenetre_macros.geometry("400x300")

        # Affichage des informations nutritionnelles
        tk.Label(fenetre_macros, text=f"Bienvenue {pseudo_utilisateur} !", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(fenetre_macros, text=f"Total kcal nécessaires: {kcal_total} kcal", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(fenetre_macros, text=f"Protéines: {proteines} g", font=("Arial", 10)).pack()
        tk.Label(fenetre_macros, text=f"Glucides: {glucides} g", font=("Arial", 10)).pack()
        tk.Label(fenetre_macros, text=f"Lipides: {lipides} g", font=("Arial", 10)).pack()

        # Bouton de déconnexion
        tk.Button(fenetre_macros, text="Se déconnecter", font=("Arial", 12), command=fenetre_macros.destroy).pack(pady=20)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Trenz Alim")
root.geometry("400x300")  # Taille de la fenêtre

# Titre
label_titre = tk.Label(root, text="Bienvenue sur Trenz Alim", font=("Arial", 16, "bold"))
label_titre.pack(pady=30)

# Bouton "Créer un compte"
btn_inscription = tk.Button(root, text="Créer un compte", font=("Arial", 12), command=ouvrir_inscription)
btn_inscription.pack(pady=10)

# Bouton "J'ai déjà un compte"
btn_connexion = tk.Button(root, text="J'ai déjà un compte", font=("Arial", 12), command=ouvrir_connexion)
btn_connexion.pack(pady=10)


root.mainloop()
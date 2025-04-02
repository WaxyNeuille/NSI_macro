"""
Fait par :
    - Jules et Lucas
Fichier qui permettra de stocker les variables, fonctions et autres bases utilitaires pour l'application.
Module : Biblo.py

les différents modules importés:
    - time
    - sleep
    - sqlite3
    - string 
    - sys

Les différentes fonctions:
    - secure_mot_de_passe
    - affichage
    - quitter
    - Verif_mdp
    - Verif_email
    - Verif_pseudo
    - Macro_manquant
    - Convert_macro_to_tuple
    - Convert_macro_to_list
    - get_id_aliment
    - get_poid_aliment
    - recherche
    - creer_Aliment
    - get_macro_alim
    - recalculer_macro
    - creer_compte
    - get_id_utilisateur
    - get_info_compte
    - modifier_utilisateur
    - get_all_macro_alim
    - get_date_aliment
    - ajouter_consommation
    - Delete_consommation
    - supprimer_consommation
    - afficher_consommation
    - get_id_alim_cons
    - get_info_activite
    - get_id_activite
    - recherche_activite
    - ajuster_cal_act
    - Besoin
    - IMC1
    - Condition_util
"""
#Importation des modules
import time # utilisation des fonction time pour éviter d'aller trop vite sur le terminal
from time import sleep # utilisation de sleep pour un affichage progressif du texte
import sqlite3 # Permet d'intéragir avec la base de données
from pprint import * # Pour l'affichage dans le terminal
import string # pour la fonction verifier mot de passe
import sys # pour un affichage progressif du texte
###########################################################################################
# définition des fonctions de calcules / vérification / affichage:

def affichage(texte:str, vitesse:float = 0.05) -> print: # FINI
    """
    Fait par : Lucas
    param :
        - le texte à afficher dans le terminal
        - la vitesse (prédefinis) a laquelle chaque lettre devra apparaître
    return :
        - rien
    """
    for lettre in texte:
        sys.stdout.write(lettre)  # Affiche une lettre sans retour à la ligne
        sys.stdout.flush()  # Force l'affichage immédiat
        time.sleep(vitesse)  # Pause entre chaque lettre
    print()  # Ajoute un retour à la ligne à la fin

def quitter(pseudo:str = None) -> print: # FINI
    if pseudo == None:
        print("Merci d'avoir utiliser gainz tracker !!")
    else:
        print(f"A très bientôt {pseudo} !!")
    print("Chargement en cours", end="")
    for i in range(5): # petite animation de chargement dans le terminal
        sleep(0.5)
        print(".", end="", flush=True)  # flush=True force l'affichage immédiat
    exit()

def secure_mot_de_passe(mot_de_passe:str) -> list: # FINI
    """
    param : 
        - mot_de_passe: Le mot de passe à vérifier
    return: 
        - Une liste vide si le mot de passe est valide, sinon une liste contenant les erreurs.
    
    Vérifie si le mot de passe respecte les critères et retourne une liste d'erreurs s'il est invalide.
    Critères :
        - Contient au moins une lettre majuscule
        - Contient au moins un chiffre
        - Contient au moins un caractère spécial

    Fait par Lucas
    """
    erreurs = []
    # Vérifie les critères
    if not any(char.isupper() for char in mot_de_passe): # Présence de majuscule
        erreurs.append("Le mot de passe doit contenir au moins une lettre majuscule.")
    if not any(char.isdigit() for char in mot_de_passe): # Présence de chiffre
        erreurs.append("Le mot de passe doit contenir au moins un chiffre.")
    caracteres_speciaux = string.punctuation # Présence de caractère spéciaux
    if not any(char in caracteres_speciaux for char in mot_de_passe):
        erreurs.append("Le mot de passe doit contenir au moins un caractère spécial.")
    # Retourne la liste des erreurs
    return erreurs

def Verif_mdp(Vmdp:str, ID:int) -> bool: # FINI
    """
    fait par : Lucas
    param :
        - Vmdp
        - ID
    renvoie :
        - True si le mot de passe est correcte
        - False si il n'est pas correct
    Fonction qui permet de verifier la correspondance d'un mot de passe
    """
    conn = sqlite3.connect("DB.db")
    curseur = conn.cursor()
    requete = "SELECT mdp FROM Utilisateurs WHERE IDutilisateur = ?"
    curseur.execute(requete, (ID,))
    resultat = curseur.fetchone()
    conn.close()
    mdp = resultat[0] #extraction du mot de passe
    if mdp == Vmdp:
        return True # Le mot de passe correspond
    else:
        return False  # Le mot de passe ne correspond pas

def Verif_email(Vemail:str, ID:int) -> bool: # FINI
    """
    Fait par : Lucas
    param :
        - Vemail 
    return :
        - True si l'email existe
        - False si l'email n'existe pas
    Fonction qui permet de vérifier la correspondance de l'email
    """
    conn = sqlite3.connect("DB.db")
    curseur = conn.cursor()
    # recherche de l'email du compte
    requete = "SELECT email FROM Utilisateurs WHERE IDutilisateur = ?"
    curseur.execute(requete, (ID,))
    resultat = curseur.fetchone()
    conn.close() # Fermer la connexion
    email = resultat[0]
    if Vemail == email:
        return True
    else:
        return False

def Verif_pseudo(Vpseudo:str , ID:int) -> bool: #FINI
    """
    Fait par : Lucas
    param :
        - Vpseudo
        - l'id de l'utilisateur
    return :
        - IDutilisateur si le pseudo existe
        - False si le pseudo n'existe pas
    Fonction qui permet de vérifier la correspondance du pseudo
    """
    conn = sqlite3.connect("DB.db")
    curseur = conn.cursor()
    # recherche du pseudo du compte
    requete = "SELECT pseudo FROM Utilisateurs WHERE IDutilisateur = ?"
    curseur.execute(requete, (ID,))
    resultat = curseur.fetchone()
    conn.close() # Fermer la connexion
    pseudo = resultat[0]
    if Vpseudo == pseudo:
        return True
    else:
        return False

def Macro_manquant(tcN:int, lN:int, gN:int, pN:int, macro_j:list) -> int: # FINI
    """
    Fait par Lucas
    param :
        - tcN (total calorique nécessaire)
        - lN (lipides nécessaire)
        - gN (glucides nécessaire)
        - pN (proteine nécessaire)
    return:
        - tcM (total calorique manquant)
        - lM (lipides manquant)
        - gM (glucide manquant)
        - pM (proteine manquant)
    Fonction qui permettra de donner les macro nutriment manquant de l'utilisateur
    """
    tcJ,lJ,pJ,gJ = Convert_Macro_to_tuple(macro_j)
    tcM = tcN - tcJ # Les calories maquante équivaut au calories nécessaire moins les calories manger
    lM = lN - lJ # système de calcul similaire sur les autres macronutriment   
    gM = gN - gJ
    pM = pN - pJ
    tcM = round(tcM)
    lM = round(lM) # pour éviter d'afficher à l'utilisateur des chiffres à ralonges
    gM = round(gM)
    pM = round(pN)
    return tcM, lM, gM, pM

def Convert_Macro_to_tuple(liste:list) -> tuple: # FINI
    """
    Fait par Lucas
    param :
        - liste de macronutriment
    return :
        - calorie
        - glucide
        - proteine
        - lipide
    Fonction qui permettra de dépackter la liste de macronutriment en variables
    """
    calorie = liste[0]
    glucide = liste[1]
    proteine = liste[2]
    lipide = liste[3]
    return calorie, glucide, proteine, lipide

def Convert_Macro_to_list(tc, g, p, l) -> list: # FINI
    """
    Fait par : Lucas
    param:
        - total calorique 
        - glucide
        - protéine
        - lipides
    return:
        - liste de macro
    Fonction qui permettra de convertir un tuple de macro en liste
    """
    lst = [tc, g, p, l]
    return lst

###########################################################################################
# Fonction pour la table Aliment

def get_id_aliment(nom_aliment:str) -> int: # FINI
    """
    Fait par : Lucas
    param :
        - le nom de l'aliment rechercher
    return :
        - l'identifiant de l'aliment dans la base de données ou None si erreur
    Récupère l'ID d'un aliment en fonction de son nom."""
    conn = sqlite3.connect("DB.db") #Connexion à la base de données
    curseur = conn.cursor()
    requete = "SELECT IDAliment FROM Aliments WHERE Nom_Aliment = ?;"
    curseur.execute(requete, (nom_aliment,))
    resultat = curseur.fetchone()  # Récupère une seule ligne
    conn.close()
    if resultat:
        return resultat[0]  # Retourne l'ID de l'aliment
    else:
        return None  # Retourne None si l'aliment n'existe pas

def get_poid_aliment(id_aliment: int): # FINI
    """
    Fait par : Lucas
    param 
        - ID de l'aliment
    return: 
        - Poids de l'aliment ou None si l'aliment n'existe pas
    Fonction qui permettra de récuperer le poids d'un aliment à partir de son ID.
    """
    conn = sqlite3.connect("DB.db")
    curseur = conn.cursor()
    curseur.execute("SELECT poid_Aliment FROM Aliments WHERE IDAliment = ?", (id_aliment,))
    resultat = curseur.fetchone()
    conn.close() # fermer la base de données
    poid = resultat[0]
    if poid:
        return poid
    else:
        None

def recherche(alim:str)->int: # FINI
    """
    Fait par : Lucas
    Paramètrage :
        - alim (aliment)
    Renvoie :
        - Nom_Aliment
    Fonction qui permet à l'utilisateur de trouver l'aliments qui correspondent à ses besoins.
    """
    conn = sqlite3.connect("DB.db")  # Connexion à la base de données
    curseur = conn.cursor()
    # Requête SQL pour rechercher les aliments correspondant au mot-clé
    requete = "SELECT * FROM Aliments WHERE Nom_Aliment LIKE ?"
    curseur.execute(requete, [f"%{alim}%"])
    resultats = curseur.fetchall()
    # Fermer la connexion
    conn.close()
    return resultats  # Retourne une liste des aliments trouvés

def creer_Aliment(nom: str, c: int, g: int, p: int, l: int, poid: float) -> int: # FINI
    """
    Fait par Lucas
    Param :
        - nom (nom de l'aliment)
        - c (calories de l'aliment)
        - g (glucide de l'aliment)
        - p (proteine de l'aliment)
        - l (lipide de l'aliment)
        - poid (poids en g de l'aliment)
    return :
        - IDAliment (l'ID de l'aliment inséré)
    Fonction qui permet d'ajouter un aliment créé par l'utilisateur dans la base de données
    et retourne l'ID attribué automatiquement.
    """
    # Verifier les variables
    if c <=0:
        raise ValueError("Les calories ne peuvent pas être inférieur ou égal à 0")
    if g <0:
        raise ValueError("Les glucides ne peuvent pas être négatif")
    if p <0:
        raise ValueError("les protéine ne peuvent pas être négatif")
    if l <0:
        raise ValueError("les lipides ne peuvent pas être négatif")
    if poid <=0:
        raise ValueError("le poid ne peut pas être égal ou inférieur à 0")
    conn = sqlite3.connect("DB.db") # Connexion à la base de données
    curseur = conn.cursor()
    # Requête SQL pour insérer l'aliment
    requete = """
    INSERT INTO Aliments (Nom_Aliment, Calories_Aliment, Glucide_Aliment, Proteine_Aliment, Lipide_Aliment, poid_Aliment)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    curseur.execute(requete, (nom, c, g, p, l, poid))
    # Récupérer l'ID du dernier aliment inséré
    id_aliment = curseur.lastrowid # sélectionne l'ID 
    conn.commit() # enregistrer les modifications
    conn.close() # fermer la base de données
    return id_aliment  # Retourne l'ID attribué si nécessaire

def get_macros_alim(id_utilisateur: int, id_aliment: int) -> list:
    """
    Fait par : Lucas
    param 
        - ID de l'utilisateur ayant consommé l'aliment.
        - ID de l'aliment consommé.
    return:
        - Une liste (calories, glucides, protéines, lipides) ou None si l'aliment n'est pas trouvé.
    Fonction qui permettra de récuperer les macronutriments d'un aliment consommé par un utilisateur.
    """
    conn = sqlite3.connect("DB.db")
    curseur = conn.cursor()
    # Requête pour récupérer les macronutriments et le poids consommé
    curseur.execute("""
        SELECT a.Calories_Aliment, a.Glucide_Aliment, a.Proteine_Aliment, a.Lipide_Aliment, c.poid_Aliment
        FROM Consommation c
        JOIN Aliments a ON c.IDAliment = a.IDAliment
        WHERE c.IDutilisateur = ? AND c.IDAliment = ?
        ORDER BY c.Date DESC LIMIT 1
    """, (id_utilisateur, id_aliment))
    resultat = curseur.fetchone()
    conn.close() # fermeture de la base de données
    if resultat:
        # Calcul des macronutriments en fonction du poids consommé
        calories, glucides, proteines, lipides, poid_consommer = resultat
        facteur = poid_consommer / 100  # Conversion pour 100g
        calories = round(calories * facteur, 2)
        glucides = round(glucides * facteur, 2)
        proteines = round(proteines * facteur, 2)
        lipides = round(lipides * facteur, 2)
        macro = [calories, glucides, proteines, lipides]
        return macro
    else:
        return [0, 0, 0, 0]

def recalculer_macros(id_utilisateur): # FINI
    """
    Fait pas : Lucas
    param :
        - l'identifiant de l'utilisateur
    return :
        - rien
    fonction qui permettra de mettre à jour la table consommation de l'utilisateur
    """
    conn = sqlite3.connect("DB.db") # Connexion à la base de données
    curseur = conn.cursor()
    # Récupérer tous les aliments consommés par l'utilisateur
    requete = """SELECT a.calories, a.proteines, a.glucides, a.lipides, c.quantite 
                 FROM Consommation c 
                 JOIN Aliments a ON c.id_aliment = a.id 
                 WHERE c.id_utilisateur = ?"""
    curseur.execute(requete, (id_utilisateur,))
    aliments = curseur.fetchall()
    # Initialisation des nouveaux macros
    total_calories = 0
    total_proteines = 0
    total_glucides = 0
    total_lipides = 0
    for calories, proteines, glucides, lipides, quantite in aliments: # Calcul des macros en fonction des aliments consommés
        total_calories += calories * quantite
        total_proteines += proteines * quantite
        total_glucides += glucides * quantite
        total_lipides += lipides * quantite
    # Mettre à jour le total calorique de l'utilisateur
    requete_update = """UPDATE Utilisateurs 
                        SET total_calories = ?, total_proteines = ?, total_glucides = ?, total_lipides = ? 
                        WHERE ID = ?"""
    curseur.execute(requete_update, (total_calories, total_proteines, total_glucides, total_lipides, id_utilisateur))
    conn.commit()

###########################################################################################
# Fonction pour la table Utilisateur

def creer_compte(pseudo:str, email:str, mdp:str, age:int, taille:int, poid:float, sex:int, objectif:int, niv_activiter:int) -> str: # FINI
    """
    fait par : Lucas
    param : 
        - pseudo de l'utilisateur
        - email de l'utilisateur
        - mdp de l'utilisateur
        - age de l'utilisateur
        - taille de l'utilisateur
        - poid de l'utilisateur
        - sex de l'utilisateur
        - objectif de l'utilisateur
        - activiter de l'utilisateur
    return : 
        - IDutilisateur
        - (-1) Si le pseudo ou l'email est déjà utilisé
    Fonction qui permet de creer un compte et de le mettre dans la base de donnée
    """
    conn = sqlite3.connect("DB.db") #Connexion à la base de données
    curseur = conn.cursor()
    # Vérifier si le pseudo ou l'email existent déjà
    curseur.execute("SELECT IDutilisateur FROM Utilisateurs WHERE pseudo = ? OR email = ?", (pseudo, email))
    if curseur.fetchone():
        conn.close()
        return -1  # Retourne -1 si le pseudo ou l'email sont déjà utilisés
    requete = """
    INSERT INTO Utilisateurs (pseudo, email, mdp, age, taille, poid, sex, objectif, niv_activiter) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    curseur.execute(requete, (pseudo, email, mdp, age, taille, poid, sex, objectif, niv_activiter))
    conn.commit()  # Sauvegarde les changements
    IDUtilisateur = curseur.lastrowid  # commande qui permet Récupérer l'ID du nouvel utilisateur
    conn.close() # Fermeture de la connexion
    return IDUtilisateur  # Retourne l'ID du compte créé

def get_id_utilisateur(pseudo: str, email: str) -> int: # FINI
    """
    Fait par : Lucas
    
    param :
        - Pseudo de l'utilisateur
        - Email de l'utilisateur
    return :
        - ID de l'utilisateur ou None si non trouvé
    Fonction qui permettra de récuperer l'ID d'un utilisateur à partir de son pseudo ou de son email.
    """
    conn = sqlite3.connect("DB.db") # connection à la base de donner
    curseur = conn.cursor()
    curseur.execute("SELECT IDutilisateur FROM Utilisateurs WHERE pseudo = ? OR email = ?", (pseudo, email))
    resultat = curseur.fetchone()
    conn.close() # fermer la base de données
    if resultat:
        return resultat[0] #renvoie l'ID de l'utilisateur
    else:
        return None # renvoie None si il n'existe pas

def get_info_utilisateur(id_utilisateur: int) -> str | int: # FINI
    """
    Fait par : Lucas
    param :
        - id_utilisateur: ID de l'utilisateur à récupérer
    return: 
        - taille
        - poid 
        - sex
        - niv_activiter
        - objectif
    Fonction qui permettra de récupèrer les informations d'un utilisateur (taille, poids, sexe, niveau d'activité, objectif).
    """
    conn = sqlite3.connect("DB.db")  # Connexion à la base de données
    curseur = conn.cursor()
    # Requête SQL pour récupérer les infos de l'utilisateur
    curseur.execute("""
        SELECT taille, poid, sex, niv_activiter, objectif 
        FROM Utilisateurs 
        WHERE IDutilisateur = ?
    """, (id_utilisateur,))
    resultat = curseur.fetchone()  # Récupère les données
    conn.close()  # Ferme la connexion
    taille = resultat[0] # dépacktage
    poid = resultat[1]
    sex = resultat[2]
    niv_activiter = resultat[3]
    objectif = resultat[4]
    if resultat:
        return taille, poid, sex, niv_activiter, objectif
    else:
        return None  # Retourne None si l'utilisateur n'existe pas

def modifier_utilisateur(id_utilisateur:int, nouveau_pseudo:str = None, nouveau_email:str = None, nouveau_mdp:str = None, nouvelle_taille:int = None, nouveau_poid:int = None, nouveau_sex:int = None, nouvel_objectif:int = None, nouveau_niv_activiter:int = None): # FINI
    """
    Fait par : Lucas
    param: 
        - ID de l'utilisateur à modifier
        - Nouveau pseudo (laisser None si pas de modification)
        - Nouveau email (laisser None si pas de modification)
        - Nouveau mot de passe (laisser None si pas de modification)
        - Nouvelle taille (laisser None si pas de modification)
        - Nouveau poid (laisser None si pas de modification)
        - Nouveau sex (laisser None si pas de modification)
        - Nouvelle objectif (laisser None si pas de modification)
        - Nouveau niveau d'activiter (laisser None si pas de modification)
    return :
        - rien
    Fonction qui permettra de modifier les données d'un utilisateur dans la base de données.
    """
    conn = sqlite3.connect("DB.db")  # Connexion à la base de données
    curseur = conn.cursor()
    if nouveau_pseudo != None:
        curseur.execute("UPDATE Utilisateurs SET pseudo = ? WHERE IDutilisateur = ?", (nouveau_pseudo, id_utilisateur))
    if nouveau_email != None:
        curseur.execute("UPDATE Utilisateurs SET email = ? WHERE IDutilisateur = ?", (nouveau_email, id_utilisateur))
    if nouveau_mdp != None:
        curseur.execute("UPDATE Utilisateurs SET mdp = ? WHERE IDutilisateur = ?", (nouveau_mdp, id_utilisateur))
    if nouvelle_taille != None:
        curseur.execute("UPDATE Utilisateurs SET taille = ? WHERE IDutilisateur = ?", (nouvelle_taille, id_utilisateur))
    if nouveau_poid != None:
        curseur.execute("UPDATE Utilisateurs SET poid = ? WHERE IDutilisateur = ?", (nouveau_poid, id_utilisateur))
    if nouveau_sex != None:
        curseur.execute("UPDATE Utilisateurs SET sex = ? WHERE IDutilisateur = ?", (nouveau_sex, id_utilisateur))
    if nouvel_objectif != None:
        curseur.execute("UPDATE Utilisateurs SET objectif = ? WHERE IDutilisateur = ?", (nouvel_objectif, id_utilisateur))
    if nouveau_niv_activiter != None:
        curseur.execute("UPDATE Utilisateurs SET niv_activiter = ? WHERE IDutilisateur = ?", (nouveau_niv_activiter, id_utilisateur))
    conn.commit()  # Enregistrement des modifications
    conn.close()  # Fermeture de la connexion
    print("Mise à jour réussie !") # message d'information

###########################################################################################
# Fonction pour la table Consommation

def get_all_macro_consommation(id_utilisateur: int) -> tuple: # FINI
    """
    Fait par : Lucas
    param 
        - ID de l'utilisateur
    return
        - Un tuple contenant toute les macronutriments
    Fonction qui permettra de récuperer le total des macronutriments et des calories de tous les aliments consommés par un utilisateur.
    """
    conn = sqlite3.connect("DB.db") # connection a la base de données
    curseur = conn.cursor()
    curseur.execute("""
        SELECT 
            SUM(A.Calories_Aliment), 
            SUM(A.Glucide_Aliment), 
            SUM(A.Proteine_Aliment), 
            SUM(A.Lipide_Aliment)
        FROM Consommation C
        JOIN Aliments A ON C.IDAliment = A.IDAliment
        WHERE C.IDutilisateur = ?
    """, (id_utilisateur,))
    result = curseur.fetchone()
    conn.close() # fermer la base de données
    tcJ = result[0] # dépacktage du résultat
    gJ = result[1]
    pJ = result[2]
    lJ = result[3]
    if result:
        return tcJ, gJ, pJ, lJ # Renvoie toute les macro journalière de la table consommation
    else:
        0, 0, 0, 0

def get_date_aliment(id_aliment: int): # FINI
    """
    Fait par : Lucas
    param 
        - ID de l'aliment
    return: 
        - La date de l'aliment ou None si l'aliment n'existe pas
    Fonction qui permettra de récuperer le poids d'un aliment à partir de son ID.
    """
    conn = sqlite3.connect("DB.db")
    curseur = conn.cursor()
    # Recherche de la date de consommation dans la table Consommation
    curseur.execute("SELECT date FROM Consommation WHERE IDAliment = ?", (id_aliment,))
    resultat = curseur.fetchone()
    conn.close()  # Fermer la connexion à la base de données
    # Vérification du résultat et retour de la date si elle existe
    if resultat:
        return resultat[0]
    return None  # Retourne None si aucun résultat trouvé

def ajouter_consommation(id_utilisateur: int, id_aliment: int, poids: float): # FINI
    """
    Fait par : Lucas

    param 
        - ID de l'utilisateur
        - ID de l'aliment consommé
        - Poids de l'aliment consommé (en grammes)
        - Date de la consommation (format YYYY-MM-DD)
    return :
        - rien
    Fonction qui permettra d'ajouter une consommation d'aliment pour un utilisateur.
    """
    conn = sqlite3.connect("DB.db") # connection à la base de données
    curseur = conn.cursor()
    curseur.execute("INSERT INTO Consommation (IDutilisateur, IDAliment, poid_Aliment, Date) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                    (id_utilisateur, id_aliment, poids))
    conn.commit() #enregistrer les modifications
    conn.close()
    print("Consommation ajoutée avec succès !")

def delete_consommation(): # FINI
    """
    Fait par : Lucas
    param :
        - rien
    return :
        - rien
    Supprime toutes les entrées de la table Consommation.
    """
    conn = sqlite3.connect("DB.db")  # Connexion à la base de données
    curseur = conn.cursor()
    curseur.execute("DELETE FROM Consommation")  # Suppression de toutes les données
    conn.commit()  # Enregistrement des modifications
    conn.close()  # Fermeture de la connexion

def supprimer_consommation(id_utilisateur: int, id_aliment: int, date: str): # FINI
    """
    Fait par : Lucas
    param 
        - id_utilisateur: ID de l'utilisateur
        - id_aliment: ID de l'aliment consommé
        - Date de la consommation à supprimer (format YYYY-MM-DD)
    return :
        - rien
    Fonction qui permettra de supprimer une consommation d'aliment pour un utilisateur à une date donnée.
    """
    conn = sqlite3.connect("DB.db") # connection à la base de données
    curseur = conn.cursor()
    curseur.execute("DELETE FROM Consommation WHERE IDutilisateur = ? AND IDAliment = ? AND Date = ?",
                    (id_utilisateur, id_aliment, date))
    conn.commit() #enregistrer les modifications
    conn.close()
    print("Consommation supprimée avec succès !")

def afficher_consommations(id_utilisateur: int) -> list: # FINI
    """
    Fait par : Lucas
    param 
        - ID de l'utilisateur
    return: 
        - Liste des consommations sous forme de tuples
    Fonction qui permettra de afficher toutes les consommations d'un utilisateur.
    """
    conn = sqlite3.connect("DB.db") # connection à la base de données
    curseur = conn.cursor()
    curseur.execute("""
        SELECT Consommation.Date, Aliments.Nom_Aliment, Consommation.poid_Aliment
        FROM Consommation
        JOIN Aliments ON Consommation.IDAliment = Aliments.IDaliment
        WHERE Consommation.IDutilisateur = ?
        ORDER BY Consommation.Date DESC
    """, (id_utilisateur,))
    consommations = curseur.fetchall()
    conn.close() # fermeture de la base de données
    return consommations  # Retourne la liste des consommations

def get_id_alim_cons(id_utilisateur: int, nom_aliment: str) -> int: # FINI
    """
    Fait par : Lucas
    param:
        - ID de l'utilisateur
        - Nom de l'aliment recherché
    return: 
        - ID de l'aliment dans la table Consommation ou None si non trouvé
    Fonction qui permettra de Récuperer l'ID d'un aliment précis consommé par un utilisateur.
    """
    conn = sqlite3.connect("DB.db") # connexion à la base de données
    curseur = conn.cursor()
    curseur.execute("""
        SELECT C.IDAliment FROM Consommation C
        JOIN Aliments A ON C.IDaliment = A.IDAliment
        WHERE C.IDutilisateur = ? AND A.Nom_Aliment = ?
    """, (id_utilisateur, nom_aliment))
    result = curseur.fetchone()  # Récupère le premier résultat
    conn.close()
    id_alim = result[0]
    if result[0]:
        return id_alim
    else:
        return None
###########################################################################################
# Fonction pour la table Activité

def get_id_activite(nom_activite: str) -> int: # FINI
    """
    Fait par : Lucas
    param :
        - nom_activite: Nom de l'activité recherchée
    return : 
        - ID de l'activité ou None si non trouvée
    Fonction qui permettra récuperer l'ID d'une activité à partir de son nom.
    """
    conn = sqlite3.connect("DB.db")  # Connexion à la base de données
    curseur = conn.cursor()
    curseur.execute("SELECT IDactivite FROM Activites WHERE type_activite = ?", (nom_activite,)) # requête SQL
    resultat = curseur.fetchone()
    conn.close() # fermeture de la base de données
    ID = resultat[0]
    if resultat[0]:
        return ID
    else:
        return None

def get_info_activite(id_activite: int) -> tuple: # FINI
    """
    Fait par : Lucas
    param 
        - ID de l'activité à rechercher
    return
        - Un tuple contenant (nom_activite, calories_brulees, duree) ou None si l'ID n'existe pas
    Fonction qui permettra de récuperer les informations d'une activité à partir de son ID.
    """
    conn = sqlite3.connect("DB.db") # connection à la base de données
    curseur = conn.cursor()
    # Requête pour récupérer uniquement les informations souhaitées
    curseur.execute("SELECT type_activite, duree, CalorieBruler FROM Activites WHERE IDactivite = ?", (id_activite,))
    resultat = curseur.fetchone()
    conn.close()  # Fermer la connexion à la base de données
    return resultat  # Retourne un tuple (nom, duree, calories_brulees) ou None si non trouvé

def recherche_activites(activiter: str) -> list: # FINI
    """
    Fait par : Lucas
    param :
        - activiter rechercher
    return :
        - Liste des noms des activités disponibles ou une liste Vide
    Fonction qui permettra de récuperer la liste des activités existantes dans la base de données.
    """
    conn = sqlite3.connect("DB.db")  # Connexion à la base de données
    curseur = conn.cursor()
    # Requête SQL pour rechercher les aliments correspondant au mot-clé
    requete = "SELECT * FROM Activites WHERE type_activite LIKE ?"
    curseur.execute(requete, [f"%{activiter}%"])
    resultats = curseur.fetchall()
    conn.close() # Fermer la connexion
    return resultats  # Retourne une liste des aliments trouvés

def ajuster_cal_act(calories_base:int, duree:int, reference_duree:int=60) -> float: # FINI
    """
    Fait par Lucas
    Ajuste les calories brûlées en fonction de la durée de l'activité.
    param :
        - calories_base (Nombre de calories brûlées pour la durée de référence (ex: 60 min))
        - duree (Durée réelle de l'activité en minutes)
        - reference_duree (Durée standard pour laquelle les calories de base sont calculées)
    return :
        - Nombre ajusté de calories brûlées
    """
    calories_base = float(calories_base)  # on convertis en flottant pour pouvoir correctement effectuer la division
    reference_duree = float(reference_duree)
    duree = float(duree)
    result = (calories_base / reference_duree) * duree # Calcule pour conversion
    return result

###########################################################################################
# Fonction de calcule de macro et autre utilitaires

def Besoin(tu:int, pu:int, sex:int, activiter:int, obj:int) -> int | list: # FINI
    """
    Fait par Lucas
    param :
        - tu (taille utilisateur)
        - pu (poid utilisateur
        - sex (sex de l'utilisateur) (1 homme) (2 femme)
        - activiter (le niveau d'activiter de l'utilisateur de 1 à 5)
        - obj  (1 perte de poid) (2 maintiens) (3 Prise de masse)
    return :
        - TDEE (l'ensemble de la consommation de l'utilisateur)
        - BMR (métabolisme basal de l'utilisateur)
        - macro_nes (liste de calories et macronutriment nécéssaire)
    Fonction qui permettra de définir la maintenance calorique de l'utilisateur en fonction de ses objectifs
    """
    if tu <= 0:
        raise ValueError("La taille doit être supérieure à 0.")
    if pu <= 0:
        raise ValueError("Le poid doit être supérieure à 0.")
    # initialisation des variables
    TDEE = 0
    BMR = 0
    if sex == 1: # calcule du Métabolisme basal (BMR)
        BMR = 447.593 + (9.247*pu) + (4.799*tu) # calcul du BMR
    elif sex == 2:
        BMR = 88.362 + (13.397*pu) + (3.098*tu) # calcul du BMR
    else:
        raise ValueError("Le sex de l'utilisateur peut sois être homme (1) sois femme(2)") # renvoie une erreur si jules fait nimp
    # cacule du TDEE
    if activiter == 1:
        TDEE = BMR*1.2
    elif activiter == 2:
        TDEE = BMR*1.375
    elif activiter == 3:
        TDEE = BMR*1.55
    elif activiter == 4:
        TDEE = BMR*1.725
    elif activiter == 5:
        TDEE = BMR*1.9
    else:
        raise ValueError("Entrez une valeur entre 1 à 5 pour le niveau d'activiter") # erreur
    # Calcule des macronutriment nécessaire selon le TDEE
    if obj == 1:
        tcN = TDEE*1.1
    elif obj == 2:
        tcN = TDEE
    elif obj == 3:
        tcN = TDEE*0.8
    else:
        raise ValueError("La variable obj doit être 1, 2 ou 3")
    # Calcul des protéines et lipides (en g)
    pN = pu * 2.2  # 2.2g de protéines par kg
    lN = pu * 0.8  # 0.8g de lipides par kg
    gN_gm = tcN - (pN + lN) # Calcul des glucides en kcal
    gN = gN_gm / 5 # Conversion des glucides en g
    tcN, lN, gN, pN = round(tcN), round(lN), round(gN), round(pN) # Arrondir les valeurs
    macro_nes = [tcN, gN, pN, lN] # liste pour utiliser plus facilement les informations
    return TDEE, BMR, macro_nes

def IMC1(tu:float, pu:float) -> int | str: #FINI
    """
    Fait par : Lucas
    Paramètrage:
        - tu (taille de l'utilisateur)
        - pu (poid de l'utilisateur)
    renvoie :
        - l'IMC 
        - l'infoIMC
        # "error_build_imc" si aucun imc ne peut être calculer
    Permettra de calculer la valeur de l'IMC et la renvoyer à l'utilisateur.
    """
    if tu <= 0:
        raise ValueError("La taille doit être supérieure à 0.")
    if pu <= 0:
        raise ValueError("Le poid doit être supérieure à 0.")
    IMC = pu / (tu ** 2)
    if IMC <= 18.5:
        IMCinfo = "Maigreur"
    elif IMC > 18.5 and IMC <= 25:
        IMCinfo = "Moyenne"
    elif IMC > 25 and IMC <= 30:
        IMCinfo = "Surpoids"
    elif IMC > 30 and IMC <= 40:
        IMCinfo = "Obésité modérée"
    elif IMC > 40 :
        IMCinfo = "Obésité morbide"
    else : 
        info = "error_build_imc" 
        info2 = "error_build_imc"
        return info, info2
    return IMC, IMCinfo

def condition_util() -> str: #FINI
    """
    Fait par: Lucas
    param:
        - nothing
    return:
        - str
    Fonction qui stockera dans différente variable les conditions d'utilisation de l'application, cela permet
    de modéliser l'affichage des articles comme on le souhaite
    """
    intro = "Bienvenue sur l'application Gainz Trackeur, votre allié pour maximiser vos gains et optimiser votre progression avec un suivi personnalisé complet ! De la diététique à l’entraînement, adaptez votre expérience selon vos objectifs. "
    intro2 = "Vous pourrez choisir et créer vos aliments et vos recettes pour suivre vos calories, afin d'accomplir tout ce que vous entreprendrez. Connaître votre Indice de Masse Corporel (IMC) vous aidera à adapter nos fonctions à vos besoins."

    partie1 = "En utilisant notre application, vous acceptez toutes nos conditions d'utilisation. En cas de refus d'adhérer à ces conditions, vous ne pourrez pas utiliser cette application."

    partie2 = "En installant Gainz Trackeur, vous reconnaissez avoir lu, compris et accepté nos conditions d'utilisation."

    partie3 = "Vous reconnaissez avoir l'âge requis d'au moins 16 ans. Si ce n'est pas le cas, vous devez obtenir le consentement d'un de vos parents."

    partie4 = "Vous vous engagez à utiliser l'application de manière responsable et légale. Cela signifie que vous ne devez pas l'utiliser à des fins frauduleuses, tenter d'accéder à des données confidentielles, ni enfreindre ces consignes."

    partie5 = "Vous êtes entièrement responsable des dommages potentiels liés à cette application."

    partie6 = "Bien que des conseils diététiques et physiques soient fournis, ceux-ci ne remplacent pas un avis médical. Avant de commencer toute activité, veuillez consulter un professionnel de la santé pour éviter tout risque en fonction de vos particularités (maladies, allergies, etc.)."

    partie7 = "Vos données personnelles sont traitées conformément à notre politique de confidentialité. Nous nous engageons à protéger vos données personnelles."

    partie8 = "Notre application peut ne pas être conforme aux lois en vigueur dans certaines régions."
    return intro, partie1, partie2, partie3, partie4, partie5, partie6,partie7, partie8
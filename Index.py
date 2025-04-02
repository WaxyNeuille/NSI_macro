"""
Fait par : Lucas
Fichier principal ou le programme doit être lancé pour la version sous terminal.
Les données de consommation de l'utilisateur seront supprimer à l'arrêt du programme
"""
# Importation des modules
from Biblio import * # Module par Gainztracker
from time import * 
import sqlite3
###########################################################################################
# Ajout de la base de données
bdd = sqlite3.connect("DB.db")
curseur = bdd.cursor()
###########################################################################################
#initialisation des variables de bases :
ID_alim :int = None
pseudo :str = "" # pseudo de l'utilisateur
mdp :str = "" # mot de passe de l'utilisateur
tcJ :int = 0  # total calorique journalier
lJ :int = 0 # lipide journalier
pJ :int = 0 # protéine journalier
gJ :int = 0 # glucide journalier
macro_j :list = [tcJ,lJ,pJ,gJ] # liste pour les transporter plus facilement
###########################################################################################

while True: # Formulaire d'acceuille
    q = input("creer un compte (1) | connecté (2) | quitter (3) | condition d'utilisation (4)")
    if q == "1": # creer un compte
        while True: # mot de passe
            mdp = input("Veuillez entrez votre mot de passe")
            lst_info = secure_mot_de_passe(mdp)
            if lst_info == []: # condition d'arrêt
                break
            else: # affichage des erreurs
                for i in range(len(lst_info)): # parcour de la liste d'erreur possible
                    print(lst_info[i])
                print("##########") #pour une meilleur visibilité sur le terminal
        age = int(input("Veuillez entrez votre age"))
        taille = int(input("Veuillez entrez votre taille"))
        poid = int(input("Veuillez entrez votre poid"))
        while True: # sex
            sex = int(input("Veuillez entrez votre sex : homme (1) | femme(2)"))
            if sex == 1 or sex == 2: # condition d'arrêt
                break
            else: # erreur
                print("veuillez entrez un chiffre entier entre 1 et 3")
        while True: # objectif
            objectif = int(input("Veuillez précisez votre objectif : sèche (1) | maintien (2) | prise de masse (3)"))
            if objectif == 1 or objectif == 2 or objectif == 3: # condition d'arrêt
                break
            else: # erreur
                print("veuillez entrez un chiffre entier entre 1 et 3")
        while True: # niveau d'activité
            niv_activiter = int(input("Veuillez noté niveaux d'activité hebdomadaire de 1 à 5"))
            if niv_activiter == 1 or niv_activiter == 2 or niv_activiter == 3 or niv_activiter == 4 or niv_activiter == 5:
                break
            else:
                print("veuillez entrez un chiffre entier entre 1 et 5")
        while True: # pseudo et email
            pseudo = input("Veuillez entrez votre pseudo")
            email = input("Veuillez entrez votre email")
            ID = creer_compte(pseudo, email, mdp, age, taille, poid, sex, objectif, niv_activiter)
            if ID == -1: # erreur
                print("Le pseudo ou l'email est déjà utiliser veuillez en saisir des nouvelles")
            else: # condition d'arrêt
                print(f"bienvenue {pseudo}")
                break
        break
    elif q == "2": # connecter à un compte
        pseudo = input("Veuillez entrer votre pseudo")
        email = input("Veuillez entrer votre email")
        ID_temp = get_id_utilisateur(pseudo, email)
        if ID_temp != None: # Si le compte existe
            mdp = input("Veuillez entrez votre mot de passe")
            if Verif_mdp(mdp, ID_temp) == True: # Si le mot de passe correspond + break
                ID = ID_temp # création de l'ID
                taille, poid, sex, niv_activiter, objectif = get_info_utilisateur(ID)
                print(f"bienvenue {pseudo} ^^")
                print("")
                break
            else: # Si l'utilisateur se trompe
                print("mot de passe invalide")
        else: # compte inexistant
            print("Aucun compte n'est associer à ses informations")
            pseudo = None
            email = None
            mdp = None
            ID = None
    elif q == "3": # quitter l'application
        quitter()
    elif q == "4": # conditions d'utilisation
        intro, partie1, partie2, partie3, partie4, partie5, partie6,partie7, partie8 = condition_util()
        affichage(intro,0.02)
        affichage(partie1,0.02)
        affichage(partie2,0.02)
        affichage(partie3,0.02)
        affichage(partie4,0.02)
        affichage(partie5,0.02)
        affichage(partie6,0.02)
        affichage(partie7,0.02)
        affichage(partie8,0.02)
    else: # erreur
        print("Veuillez entrez une valeur entre 1 et 5")

delete_consommation()

while True: # formulaire d'interaction avec la base
    print("#############")
    print("") # saut de ligne dans le terminale
    imc, imc_info = IMC1(taille, poid) # calcule de l'imc de l'utilsateur
    imc = round(imc)
    TDEE, BMR, macro_nes = Besoin(taille, poid, sex, niv_activiter, objectif) # cacule des besoin en macronutriment
    tcN, gN, pN, lN = Convert_Macro_to_tuple(macro_nes) # extraction des macros en variables
    print(f"total calorique : {tcJ}/{tcN}")
    print(f"glucide : {gJ}/{gN} | protéines : {pJ}/{pN} | lipides : {lJ}/{lN}")
    print(f"imc {imc} : {imc_info}")
    print("######")
    q2 = input("informations du compte(1) | consommations(2) | activiter(3) | condition d'utilisation(4) | quitter(5)")
    if q2 == "1": # affichage et modification des informations du compte
        while True: # mini formulaire
            print("#############")
            print("") # saut de ligne dans le terminale
            choix0 = int(input("Changer les informations du compte(1) | changer les macros de l'utilisateur(2) | retour(3)"))
            if choix0 == 1: # change pseudo / mdp / mail + affiche
                verification = input("Entrez votre mot de passe actuelle pour acceder à ses fonctions")
                if Verif_mdp(verification, ID) == True: # verifier si le mot de passe correspond à l'ID de l'utilisateur
                    while True: # mini formulaire
                        choix3 = int(input("Que voulez vous modifier pseudo(1) | email(2) | mot de passe(3) | retour (4)"))
                        if choix3 == 1: # changement de pseudo
                            new_pseudo = input("Veuillez entrez votre nouveau pseudo")
                            print(f"votre mot de pseudo actuelle est {pseudo}")
                            modifier_utilisateur(ID, new_pseudo)
                            print("")
                            pseudo = new_pseudo
                        elif choix3 == 2: # changement de l'email
                            new_email = input("Veuillez entrez votre nouveau mail")
                            print(f"votre mot de email actuelle est {email}")
                            modifier_utilisateur(ID, new_email)
                            email = new_email
                            print("")
                        elif choix3 == 3: # changement du mot de passe
                            new_mdp = input("Veuillez entrez votre nouveau mot de passe")
                            print(f"votre mot de mot de passe actuelle est {mdp}")
                            modifier_utilisateur(ID, new_mdp)
                            mdp = new_mdp
                            print("")
                        elif choix3 == 4: #retour (break)
                            break
                        else: #erreur
                            print("Veuillez entrez une valeur valide")
                else: # erreur mot de passe invalide
                    print("mot de passe invalide")
            elif choix0 == 2: # change  imc et besoin
                while True: # mini formulaire
                    choix2 = int(input("changer manuellement les macros(1) | redéfinir le poid/taille(2) | retour(3) "))
                    if choix2 == 1: # modificaiton manuelle des macronutriments
                        affichage("attention changer manuellement ses besoins en macronutriment est fortement déconseiller")
                        while True: # mini formulaire
                            choix4 = int(input("Que voulez vous modifier : total calorique(1) | glucide(2) | protéine(3) | lipides(4) | retour(5)"))
                            if choix4 == 1: # changer calories
                                print(f"Votre apport actuelle en calories est de {tcN}")
                                tcN = int(input("Entre votre nouveau total calorique"))
                                print("Vous pouvez toujours remettre vos macro à jour à n'importe qu'elle moment")
                            elif choix4 == 2: # changer glucide
                                print(f"Votre apport actuelle en glucide est de {gN}")
                                tcN = int(input("Entre votre nouvelle apport en glucide"))
                                print("Vous pouvez toujours remettre vos macro à jour à n'importe qu'elle moment")
                            elif choix4 == 3: # changer prot
                                print(f"Votre apport actuelle en calories est de {pN}")
                                tcN = int(input("Entre votre nouvelle apport en protéine"))
                                print("Vous pouvez toujours remettre vos macro à jour à n'importe qu'elle moment")
                            elif choix4 == 4: # changer lipides
                                print(f"Votre apport actuelle en calories est de {lN}")
                                tcN = int(input("Entre votre nouvelle apport en lipides"))
                                print("Vous pouvez toujours remettre vos macro à jour à n'importe qu'elle moment")
                            elif choix4 == 5: # retour
                                break
                            else: # erreur
                                print("Erreur Veuillez selectionner une valeur entre 1 et 5")
                    elif choix2 == 2: # changement de la taille et du poid de l'utilisateur
                        taille = int(input("Veuillez entre votre taille"))
                        poid = int(input("Veuillez entrez votre poid"))
                        while True: # niveau d'activité
                            niv_activiter = int(input("Veuillez noté niveaux d'activité hebdomadaire de 1 à 5"))
                            if niv_activiter == 1 or niv_activiter == 2 or niv_activiter == 3 or niv_activiter == 4 or niv_activiter == 5: # conditions d'arrêt
                                break
                            else: # erreur
                                print("veuillez entrez un chiffre entier entre 1 et 5") 
                        while True: # objectif
                            objectif = int(input("Veuillez précisez votre objectif : sèche (1) | maintien (2) | prise de masse (3)"))
                            if objectif == 1 or objectif == 2 or objectif == 3: # condition d'arrêt
                                break
                            else: # erreur
                                print("veuillez entrez un chiffre entier entre 1 et 3")
                        modifier_utilisateur(ID, None, None, None, taille, poid, None, objectif, niv_activiter)
                        imc,imc_info = IMC1(taille, poid) # calcule de l'imc de l'utilsateur
                        TDEE, BMR, macro_nes = Besoin(taille, poid, sex, niv_activiter, objectif) # cacule des besoin en macronutriment
                        tcN, gN, pN, lN = Convert_Macro_to_tuple(macro_nes) # extraction des macros en variables
                    elif choix2 == 3: # retour (break)
                        print("") # saut de ligne
                        break
                    else: #erreur
                        print("Veuillez entrez une valeur valide entre 1 et 3 ")
            elif choix0 == 3: # retour (break)
                print("") # saut de ligne dans le terminal
                break
            else: # erreur
                print("Veuillez entrez une valeur valide entre 1 et 3")
    elif q2 == "2": # les statistique de consomation de l'utilisateur
        while True: # mini formulaire consomation
            print("#############")
            print("") # saut de ligne dans le terminale
            print(f"total calorique : {tcJ}/{tcN}")
            print(f"glucide : {gJ}/{gN} | protéines : {pJ}/{pN} | lipides : {lJ}/{lN}")
            choix1 = int(input("trouver des aliments(1) | consommer un aliment(2)| supprimer un aliment(3) | creer un aliment (4) | retour (5)"))
            if choix1 == 1: # recherche d'aliment
                mot_cle = input("entrez le nom de l'aliment que vous voulez recherche  ")
                aliments_trouves = recherche(mot_cle)
                if aliments_trouves: # affiche la liste des aliments trouver
                    print(" Aliments trouvés :")
                    print("##################################################")
                    for aliment in aliments_trouves:
                        print(aliment)
                    print("##################################################")
                    print("##################################################")
                else: # erreur aucun aliment trouver
                    print("Aucun aliment trouvé.")
            elif choix1 == 2: # consommer des aliments
                alim_cons = input("Entrez le nom exact de l'aliment que vous voulez consommer")
                ID_alim = get_id_aliment(alim_cons)
                if ID_alim == None: # cas ou l'aliment n'est pas trouver
                    print("l'aliment n'existe pas")
                    ID_alim = None
                else : # cas ou l'aliment est consommer
                    poid_alim = int(input("Veuillez entrez le poid de l'aliment"))
                    ajouter_consommation(ID, ID_alim, poid_alim)
                    macro = get_macros_alim(ID, ID_alim)  # Récupération des données
                    tcJ += macro[0]
                    gJ += macro[1]
                    pJ += macro[2]
                    lJ += macro[3]
            elif choix1 == 3: # supprimer des aliments déjà consommer
                list_cons = afficher_consommations(ID)
                print("Liste de consommation")
                print(list_cons)
                choix6 = input("Qu'elle aliments voulez-vous supprimer ?")
                ID_alim = get_id_alim_cons(ID, choix6)
                if ID_alim == None: # Cas ou l'aliment ne se trouve pas dans la table
                    print("Vous n'avez pas consommer cette aliment")
                else: #suppression de l'aliment et des info de variables
                    date = get_date_aliment(ID_alim)
                    supprimer_consommation(ID, ID_alim, date)
                    print("L'aliment à été correctement supprimer")
                    tcJ, gJ, pJ, lJ = get_all_macro_consommation(ID)
                    if tcJ == None: # question de sécurité
                        tcJ = 0
                    if gJ == None:
                        gJ = 0
                    if pJ == None:
                        pJ = 0
                    if lJ == None:
                        lJ = 0
            elif choix1 == 4: # creer un aliment
                nom_alim = input("Veuillez entrez le nom de votre aliment ")
                cal_alim = int(input("Veuillez entrez les calories de votre aliment "))
                glu_alim = int(input("Veuillez entrez les glucides de votre aliment "))
                prot_alim = int(input("Veuillez entrez proteine de votre aliment "))
                lip_alim = int(input("Veuillez entrez les lipides de votre aliment"))
                poid_alim = int(input("Veuillez entrez le poid de votre aliment"))
                ID_alim = creer_Aliment(nom_alim, cal_alim, glu_alim, prot_alim, lip_alim, poid_alim)
                if ID_alim != None: #informer sur la création de l'aliment
                    print(f"{nom_alim} a bien été creer")
                else: # bug l'aliment na pas pu etre creer 
                    print("votre aliment n'a pas été creer")
            elif choix1 == 5: # quitter la page
                break
            else: #erreur
                print("Veuillez entrez une valeur correcte")
    elif q2 == "3": # ajoute des activiter de consommation de calories
        activiter_en_cour = None
        while True:
            print("#############")
            print("") # saut de ligne dans le terminale
            if activiter_en_cour == None: # affichage des activité
                print("aucune activiter en cour")
            else: # affichage des activité
                print(f"Activiter réaliser : {activiter_en_cour}")
            choix5 = int(input("rechercher des activiter(1) | inserer une activiter(2) | retour(3)"))
            if choix5 == 1: # recherche des activité
                mot_cle = input("entrez le nom de l'activiter que vous voulez rechercher ")
                activiter_trouves = recherche_activites(mot_cle)
                if activiter_trouves: # affiche la liste des aliments trouver
                    print(" activiter trouvés :")
                    print("##################################################")
                    for act in activiter_trouves:
                        print(act)
                    print("##################################################")
                    print("##################################################")
                else: # erreur aucune activiter trouver
                    print("Aucune activiter trouvé.")
            elif choix5 == 2: # insertion d'une activité
                nom_act = input("entrez le nom exact de l'activiter")
                ID_act = get_id_activite(nom_act)
                if ID_act == None: # message d'erreur
                    print("Cette activiter n'existe pas")
                else: # ajout de l'activiter
                    activiter_en_cour = nom_act
                    duree_ult = input("Entre la duree de votre activiter")
                    activiter, duree, calories = get_info_activite(ID_act)
                    calories = ajuster_cal_act(calories, duree_ult, duree)
                    tcJ -= calories
                    print(f" vous avez dépenser :{calories} cal")
            elif choix5 == 3: # retour (break)
                print("")
                break
            else:
                print("Erreur")
    elif q2 == "4": # condition d'utilisation
        print("#############")
        print("") # saut de ligne dans le terminale
        intro, partie1, partie2, partie3, partie4, partie5, partie6,partie7, partie8 = condition_util()
        affichage(intro,0.01)
        affichage(partie1,0.01)
        affichage(partie2,0.01)
        affichage(partie3,0.01)
        affichage(partie4,0.01)
        affichage(partie5,0.01)
        affichage(partie6,0.01)
        affichage(partie7,0.01)
        affichage(partie8,0.01)
    elif q2 == "5": # quitter l'application
        quitter(pseudo)
    else: # erreur
        print("Veuillez entrez une valeur entre 1 et 5")
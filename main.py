# Imports

import os 
import numpy as np
from random import randint

# Objets

class style():
  """
  Permet l'affichage du texte avec formatage couleurs, gras, ...
  """
  BLACK = "\033[30m"
  RED = "\033[31m"
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  BLUE = "\033[34m"
  MAGENTA = "\033[35m"
  CYAN = "\033[36m"
  WHITE = "\033[37m"
  UNDERLINE = "\033[4m"
  RESET = "\033[0m"
  BOLD = "\033[1m"
class joueur():
  """
  Objet joueur contenant toutes les informations d'un joueur (nom, stats, bateaux, essais, ...)
  Paramètres :
  - pseudo : String contenant le nom de joueur
  - bateaux : Liste d'objets bateau correspondant aux bateaux du joueur
  - grilles_bateaux : Matrice représentant la position de ses bateaux affectés de leurs numéro
  - grilles_essais : Matrice représentant les anciens essais de tir du joueur affectés de la légende
  - partie : objet partie dans lequel le joueur est inclus
  """
  pseudo = ""
  bateaux = []
  grille_bateaux = []
  grille_essais = []
  partie = 0
  def __init__(self, pseudo, bateaux, grille_bateaux=[], grille_essais=[], partie=0): # Création d'un objet joueur et affectation des paramètres
    self.pseudo = pseudo
    self.bateaux = bateaux.copy()
    self.grille_bateaux = grille_bateaux
    self.grille_essais = grille_essais
    self.stats = C_stats.copy()
  def voir_bateaux(self): # Affiche sa grille bateaux
    affichage(self.grille_bateaux)
  def voir_essais(self): # Affiche sa grille essais
    affichage(self.grille_essais)
  def link_partie(self, partie): # Lie au joueur un objet partie (la partie dans laquelle il joue)
    self.partie = partie
class bateau():
  """
  Objet bateau contenant toutes les informations d'un bateau (longueur, vie, position, ...)
  Paramètres :
  - longueur : int fixe correspondant à la longueur en cases du bateau
  - vie : int variable qui correspond à la vie du bateau, son nombre de cases non touchées
  - n : int correspondant à la ligne du bateau
  - m : int correspondant à la colonne du bateau
  - pos : String h ou v indiquant l'orientation du bateau dans la grille bateau
  A noter qu'avec pos, n et m, le bateau sait exactement quelles cases il occupe dans la grille bateau
  """
  longueur=0
  vie=0
  n = 0
  m = 0
  pos = "0"
  def __init__(self,longueur): # Création d'un objet bateau
    self.longueur=longueur
    self.vie=longueur # Lors de l'initialisation, sa vie commence par sa longueur (pas encore de cases touchées)
  def set_emplacement(self, n, m, pos): # Indique au bateau sa position
    self.n = n
    self.m = m
    self.pos = pos
  def touche(self, tireur): # Si bateau touché
    self.vie -= 1 # On retire 1 à sa vie
    if self.vie == 0: # Si il n'a plus de vie, donc plus de cases, il est coulé
      print("Bateau coulé !")
      # Ce qui suit remplace toutes les cases occupées par le bateau dans la grille essais du tireur par la légende correspondant à coulé (remplace les légendes tirés précédentes + la derniere case qui vient d'être touchée)
      if self.pos == "h":
        tireur.grille_essais[self.n-1, self.m-1:self.m-1+self.longueur] = C_legende["Coulé"]*np.ones(tireur.grille_essais[self.n-1, self.m-1:self.m-1+self.longueur].shape)
      else:
        tireur.grille_essais[self.n-1:self.n-1+self.longueur, self.m-1] = C_legende["Coulé"]*np.ones(tireur.grille_essais[self.n-1:self.n-1+self.longueur, self.m-1].shape)
      return C_legende["Coulé"] # Renvoie à tir la légende coulé
    else:
      print("Bateau touché !")
      return C_legende["Touché"] # Renvoie à tir la légende tiré
class partie():
  """
  Objet partie contenant toutes les informations d'une partie (joueurs, taille grille, ...)
  Paramètres :
  - id : int fixe correspondant à l'identifiant de la partie
  - j1 : objet joueur correspondant au premier joueur de la partie
  - j2 : objet joueur correspondant au second joueur de la partie
  - taille : int correspondant à la taille des grilles de la partie
  - one_player : Boolean True s'il s'agit d'une partie un joueur / False le cas contraire
  """
  id = 0
  j1=0
  j2=0
  taille = 0
  one_player = False
  def __init__(self, nom_j1, nom_j2 ,bateaux, taille, one_player): # Création de l'objet partie
    self.j1 = joueur(nom_j1, C_bateaux[0], np.zeros((taille,taille)), np.zeros((taille,taille)), self) # Création des objets joueur
    self.j2 = joueur(nom_j2, C_bateaux[1], np.zeros((taille,taille)), np.zeros((taille,taille)), self)
    self.taille = taille
    self.id = id(self)
    self.one_player = one_player
    print(f"Partie Initialisé, {self.j1.pseudo} et {self.j2.pseudo} s'affrontent sur une grille de taille {taille} !")

# Constantes

C_bateaux = [[bateau(2),bateau(2),bateau(3),bateau(4),bateau(5)],[bateau(2),bateau(2),bateau(3),bateau(4),bateau(5)]] # Liste des bateaux de la partie pour joueur 1 et 2
C_legende = {"Loupé": 1, "Touché" : 2, "Coulé": 3} # Légende des grilles
C_couleurs = {0:style.WHITE,1:style.YELLOW,2:style.RED,3:style.GREEN,4:style.BLUE,5:style.MAGENTA,6:style.CYAN}
C_stats = {"tours" : 0, "loupe": 0, "touche": 0, "coule": 0} # Dictionnaire de référence statistiques

# Fonctions

def selection(message, max):
  """
  Permet la sélection par le joueur d'un entier compris en 1 et la valeur maximale
  Entrées :
  - message : String correspondant au message à afficher
  - max : int correspondant à la valeur maximamle acceptable (incluse)
  Sortie :
  - nb : int de la valeur saisie par l'utilisateur
  """
  valide = False 
  while valide == False: # Tant que la saisie ne remplit pas les critères
    try: # Evite l'erreur si entrée d'un autre type que int
      nb =int(input(f"{message} (1 à {max}) : "))
      if nb < 1 or nb > max: 
        print(f"Veuillez saisir une réponse valide entre 1 et {max}")
      else:
        valide = True
    except: 
      print("Veuillez renter une valeur valide")
  return nb
def pause(message="Entrée pour continuer"):
  """
  Permet de marquer une pause dans l'affichage
  Affichage d'un message et attente d'appui sur touche Entrée pour continuer
  Entrée :
  - message : String du message à afficher
  """
  input(message)
  clearConsole()
def clearConsole():
  """
  Permet de supprimer tout le texte de la console
  Plus agréable car supprime les anciens affichage
  """
  command = 'clear' # Commande clear
  if os.name in ('nt', 'dos'):  # Si la machine est sur Windows, on utilise la commande cls
    command = 'cls'
  os.system(command) # Exécution de la commande
def init(one_player=False):
  """
  Permet d'initialiser une nouvelle partie en demandant tout les paramètres nécessaires
  Entrées : 
  - one_player : Boolean True si la partie à créer est une partie 1 joueur / False le cas contraire
  Sortie :
  - objet partie correspondant à la partie crée
  """
  print("-----Nouvelle Partie-----")
  nom_j1 = input("Nom du joueur 1 : ") # Demande du nom du joueur 1
  if nom_j1 == "": # Si aucune saisie, nom par défaut
      nom_j1 = "Joueur 1"
  if one_player: # Si partie un joueur, fixe le nom de l'ordinateur et pas de demande de pseudo pour joueur 2
    nom_j2 = "l'ordinateur"
  else:
    nom_j2 = input("Nom du joueur 2 : ") # Demande du nom du joueur 2
    if nom_j2 == "": # Si aucune saisie, nom par défaut
      nom_j2 = "Joueur 2"
  valide = False
  while valide == False: # Tant que saisie non valide
    try: # Evite l'erreur en cas de saisie d'un type autre que int
      taille = input("Veuillez chosir la taille de la grille (10) : ") 
      if taille == "": # Si aucune saisie, taille 10 par défaut
        taille = 10
        valide = True
      elif int(taille)<5 or int(taille)>10: # Si taille trop petite ou trop grande
        print("La taille de la grille doit être superieure à 4 et inferieure à 11")
      else: # Si saisie valide, affectation de taille à la valeur souhaitée
        taille = int(taille)
        valide = True 
    except:
      print("Veuillez rentrer une valeur valide")
  return partie(nom_j1, nom_j2, C_bateaux, taille, one_player) # Création et renvoie de l'objet partie
def placement(joueur):
  """
  Permet au joueur entré en paramètre de placer ses bateaux dans sa grille
  Entrée :
  - joueur : objet joueur correspondant au joueur qui va placer ses bateaux
  """
  grille = joueur.grille_bateaux # Affectation de grille à la grille bateaux du joueur
  print(f"-----{joueur.pseudo} vous allez placer vos bateaux-----")
  pause()
  for i in range(len(joueur.bateaux)): # Pour chaque bateau dans sa liste de bateaux
    bateau = joueur.bateaux[-1-i] # Affecte à bateau l'objet bateau en fonction de l'indice i en partant du dernier bateau, le plus grand, afin de de faciliter le placement de ce dernier (plus de possibilité de placement)
    valide = False
    while valide == False: # Tant que le placement n'est pas valide
      print(f"-----Placement des bateaux pour {joueur.pseudo}-----")
      print("-----Grille acutuelle-----")
      affichage(grille) # Affichage de sa grille actuelle (avec les bateaux placés précédemment)
      print("----------")
      print(style.UNDERLINE + style.BOLD + f"Vous allez placer un bateau de taille {bateau.longueur}" + style.RESET) # Précise la longueur du bateau en cours de placement
      print("----------")
      direction = input("Voulez vous placer votre bateau horizontalement ou verticalement h/v : ") # Demande du choix de l'orientation
      while direction.lower() != "v" and direction.lower() != "h": # Redemander tant que choix non valide
        print("Veuillez saisir une réponse valide (h ou v)")
        direction = input("Voulez vous placer votre bateau horizontalement ou verticalement h/v : ")
      n, m = -1, -1
      if direction.lower() == "h":
        n = selection("Dans quelle ligne voulez-vous placer votre bateau", grille.shape[0]) # Demade de sélection de la ligne de placement en prenant en compte la nombre max de lignes
        m = selection("Dans quelle colonne voulez-vous placer la case gauche de votre bateau", grille.shape[1]-bateau.longueur+1) # Demade de sélection de la colonne de placement de la gauche du bateau en prenant en compte la nombre max de colonnes et la taille du bateau
        if sum(grille[n-1, m-1:m-1+bateau.longueur]) != 0: # Si un bateau occupe déja les positions choisies
            print("Un bateau occupe déja une des positions souhaitées, veuillez changer votre localisation")
            input("Entrée pour continuer")
            valide = False
            clearConsole()
        else: # Si pas de bateau ici
          grille[n-1, m-1:m-1+bateau.longueur] = (len(joueur.bateaux)-i)*np.ones(grille[n-1, m-1:m-1+bateau.longueur].shape) # Remplace dans la grille bateaux les cases concernées par le numéro du bateau (le premier est 1 et non 0)
          bateau.set_emplacement(n, m, "h") # Avertit l'objet bateau de son emplacement
          valide = True
      else:
        m = selection("Dans quelle colonne voulez-vous placer votre bateau", grille.shape[1]) # Demade de sélection de la colonne de placement en prenant en compte la nombre max de colonnes
        n = selection("Dans quelle ligne voulez-vous placer le haut de votre bateau", grille.shape[0]-bateau.longueur+1) # Demade de sélection de la ligne de placement du haut du bateau en prenant en compte la nombre max de lignes et la taille du bateau
        if sum(grille[n-1:n-1+bateau.longueur, m-1]) != 0: # Si un bateau occupe déja les positions choisies
            print("Un bateau occupe déja une des positions souhaitées, veuillez changer votre localisation")
            input("Entrée pour continuer")
            valide = False
            clearConsole()
        else: # Si pas de bateau ici
          grille[n-1:n-1+bateau.longueur, m-1] = (len(joueur.bateaux)-i)*np.ones(grille[n-1:n-1+bateau.longueur, m-1].shape) # Remplace dans la grille bateaux les cases concernées par le numéro du bateau (le premier est 1 et non 0)
          bateau.set_emplacement(n, m, "v") # Avertit l'objet bateau de son emplacement
          valide = True 
    print("Bateau placé avec succès") # Bateau placé
    pause()
    # Bateau placé
  # Tous les bateaux placés
  print(f"-----Tous vos bateaux sont placés {joueur.pseudo}-----")
  print("Voici votre grille finale : ")
  affichage(grille) # Affichage de la grille avec tous les bateaux placés
  print("----------")
def placement_alea(joueur):
  """
  Gère le placement aléatoire des bateaux de l'ordinateur dans sa grille bateaux
  Entrée :
  - joueur : objet joueur correspondant à l'ordinateur
  """
  orientation=["h","v"]
  grille = joueur.grille_bateaux # Récupère la grille bateaux de l'ordinateur
  for i in range(len(joueur.bateaux)): # Pour chaque objet bateau de l'ordinateur
    bateau = joueur.bateaux[-1-i] # Affecte à bateau l'objet bateau en fonction de l'indice i en partant du dernier bateau, le plus grand, afin de de faciliter le placement de ce dernier (plus de possibilité de placement)
    placement_valide=False
    while not placement_valide: # Tant que le placement n'est pas valide
      direction=orientation[randint(0,1)] # Choix d'une orientation aléatoire
      n, m = -1, -1
      if direction == "h": # Si placement horizontal
        n=randint(1,grille.shape[0]) # Choix d'un numéro de ligne aléatpore entre 1 et le nombre de lignes de la grille
        m=randint(1,grille.shape[1]-bateau.longueur+1) # Choix aléatoire de la colonne de la gauche du bateau en prenant en compte sa longueur
        if sum(grille[n-1, m-1:m-1+bateau.longueur]) == 0: # Si il n'existe pas déjà de bateaux sur les cases que va occuper le bateau
          grille[n-1, m-1:m-1+bateau.longueur] = (len(joueur.bateaux)-i)*np.ones(grille[n-1, m-1:m-1+bateau.longueur].shape) # Remplace dans la grille bateaux les cases concernées par le numéro du bateau (le premier est 1 et non 0)
          bateau.set_emplacement(n, m, "h") # Avertit l'objet bateau de son emplacement
          placement_valide = True
      else:
          m = randint(1,grille.shape[1]) # Choix d'un numéro de ligne aléatpore entre 1 et le nombre de colonnes de la grille
          n = randint(1,grille.shape[0]-bateau.longueur+1) # Choix aléatoire de la ligne du haut du bateau en prenant en compte sa longueur
          if sum(grille[n-1:n-1+bateau.longueur, m-1]) == 0: # Si il n'existe pas déjà de bateaux sur les cases que va occuper le bateau
            grille[n-1:n-1+bateau.longueur, m-1] = (len(joueur.bateaux)-i)*np.ones(grille[n-1:n-1+bateau.longueur, m-1].shape) # Remplace dans la grille bateaux les cases concernées par le numéro du bateau (le premier est 1 et non 0)
            bateau.set_emplacement(n, m, "v") # Avertit l'objet bateau de son emplacement
            placement_valide = True 
  print(f"-----Tous les bateaux de l'ordinateur sont placés-----")
def affichage(grille):
  """Permet ici de modifier la manière d'afficher les grilles
  Affecte l'affichage des grille de tout le programme
  """
  ligne = "   |  "
  for j in range(grille.shape[1]):
    ligne += (str(j+1) + "  ")
  print(style.BOLD + ligne)
  tirets = ""
  for p in range(len(ligne)):
    tirets += "-"
  print(style.BOLD + tirets)
  for i in range(grille.shape[0]):
    if i>= 9:
      print(style.BOLD + str(i+1) + " |  ", end = '')
    else:
      print(style.BOLD + str(i+1) + "  |  ", end = '')
    for k in range (len(grille[i])):
        element = grille[i][k]
        print(style.RESET + C_couleurs[element]+ str(int(element)) + "  ", end = '')
    print(style.RESET + "")
def roulement(partie):
  """
  Exécute, après avoir désigné un premier joueur, l'alternance des tours avec prise en charge des rejouer jusqu'à fin de partie
  Entrée :
  - partie : objet partie de la partie concernée
  """
  current = 0 # Variable désignant le joueur dont c'est le tour
  if randint(1,2) == 1: # Désignation aléatoire du premier joueur et affectation à current
    current = partie.j1
  else:
    current = partie.j2
  print(f"Part tirage au sort, c'est {current.pseudo} qui commence !")
  pause()
  # Roulement des tours
  while np.any(partie.j1.grille_bateaux) != 0 and np.any(partie.j2.grille_bateaux) != 0: # Tant que les deux joueurs ont encore des bateaux
    if current == partie.j1: # Si c'est au joueur 1 de jouer
      if not tour(partie.j1, partie.j2, partie.one_player): # Exécution du tour de j1
        current = partie.j2 # Affectation de current au joueur 2 si il ne rejoue pas
    else:
      if not tour(partie.j2, partie.j1, partie.one_player): # Exécution du tour de j2
        current = partie.j1 # Affectation de current au joueur 1 si il ne rejoue pas
  print("Partie terminée")
  if np.any(partie.j1.grille_bateaux) == 0: # Si c'est joueur 1 qui n'a plus de bateaux
    print(f"{partie.j2.pseudo} gagne la partie")
  else: # Sinon (joueur 2 n'a plus de bateaux)
    print(f"{partie.j1.pseudo} gagne la partie")
  for player in [partie.j1, partie.j2]: # Affichage des statistiques pour les deux joueurs
    print(f"-----Statistiques de {player.pseudo}-----")
    print(f'Nombre de tirs : {player.stats["tours"]}')
    print(f"Nombre de loupé : {player.stats['loupe']}")
    print(f"Nombre de touché : {player.stats['touche']}")
    print(f"Nombre de bateaux adverses coulés : {player.stats['coule']}")
    print(f'Efficacité des tirs : {player.stats["touche"]/player.stats["tours"]*100:.2f} %')  
def roulement_solo(partie):
  """
  Exécuter le roulement des tours pour une partie 1 joueur
  Entrée :
  - partie : objet partie de la partie concernée
  """
  while np.any(partie.j2.grille_bateaux) != 0: # Tant que l'ordinateur à encore des bateaux
    tour(partie.j1, partie.j2, partie.one_player) # Le joueur enchaine les tours
  # Affichage des statistiques
  print("Partie terminée")
  print(f"-----Statistiques de {partie.j1.pseudo}-----")
  print(f'Nombre de tirs : {partie.j1.stats["tours"]}')
  print(f"Nombre de loupé : {partie.j1.stats['loupe']}")
  print(f"Nombre de touché : {partie.j1.stats['touche']}")
  print(f"Nombre de bateaux adverses coulés : {partie.j1.stats['coule']}")
  print(f'Efficacité des tirs : {partie.j1.stats["touche"]/partie.j1.stats["tours"]*100:.2f} %')
def tour(joueur, adversaire, one_player):
  """
  Déclanche le déroulement complet d'un tour de joueur
  Entrées :
  - joueur : objet joueur qui joue le tour
  - adversaire : objet joueur qui est l'adversaire
  - one_player : boolean True si il s'agit d'une partie 1 joueur / False si partie 2 joueurs
  Sorties :
  - rejouer : boolean True si le joueur rejoue après / False si il ne rejoue pas
  """
  if not one_player: # Uniquement si partie 2 joueurs
    # Affichage de sa grille bateaux
    print(f"{joueur.pseudo} c'est à vous de jouer")
    input("Entrée pour continuer")
    print("----------")
    print("Voici la grille de vos bateaux encore à l'eau")
    affichage(joueur.grille_bateaux)
    print("----------")
  print("Voici la grille de vos précédentes tentatives")
  affichage(joueur.grille_essais) # Affichage grille essais ainsi que de la légende
  print(f"Légende : Non visé = 0, Loupé = {style.YELLOW + str(C_legende['Loupé']) + style.RESET}, Touché = {style.RED + str(C_legende['Touché']) + style.RESET}, Coulé = {style.GREEN + str(C_legende['Coulé']) + style.RESET}")
  print("----------")
  ligne = selection("Dans quelle ligne voulez-vous tirer ?", adversaire.grille_bateaux.shape[0]) # Sélection de la ligne de tir
  colonne = selection("Dans quelle colonne voulez-vous tirer ?", adversaire.grille_bateaux.shape[1]) # Sélection de la colonne de tir
  rejouer = tir(joueur, adversaire, ligne, colonne) # Exécution de la fonction tir en fonction paramètres précédents
  if not one_player:
    if rejouer:
      print("Vous pouvez rejouer")
    else:
      print("Votre tour est terminé")
  pause()
  joueur.stats["tours"] += 1 # Ajout aux stats du joueur un tour
  return rejouer # Renvoie à roulement si le joueur doit rejouer
def tir(joueur, cible, ligne, colonne):
  """Permet d'analyser le résultat d'un tir
  Entrées :
  - joueur : objet joueur qui effectue le tir
  - cible : objet joueur qui est l'objet du tir
  - ligne : entier correspondant au numéro de ligne du tir
  - colonne : entier correspondant au numéro de colonne du tir
  Sorties :
  - Boolean : True si le joueur peut rejouer, False le cas inverse
  """
  if joueur.grille_essais[ligne-1, colonne-1] != 0: # Si la case est différente de 0 dans la grille de ces essais (déja tiré ici)
    print("Vous aviez déjà tiré ici :/")
    joueur.stats["loupe"] += 1 # Ajout aux stats du joueur un tir loupé
    return False # Il ne rejoue pas
  elif cible.grille_bateaux[ligne-1, colonne-1] == 0: # Si un 0 présent dans la grille des bateaux de l'adversaire (aucun bateau flottant)
    print("C'est un tir loupé...")
    joueur.stats["loupe"] += 1 # Ajout aux stats du joueur un tir loupé
    joueur.grille_essais[ligne-1, colonne-1] = C_legende["Loupé"] # Mise du chiffre correspondant à loupé dans la grille essai du joueur
    return False # Il ne rejoue pas
  else: # Si chiffre présent dans la grille bateaux de la cible
    indice = cible.grille_bateaux[ligne-1, colonne-1] # Récupère le numéro du bateau adverse touché
    result = cible.bateaux[int(indice)-1].touche(joueur) # Appel de la fonction touché du bateau adverse concerné. Renvoie la valeur à retourner dans la grille essai du joueur
    joueur.grille_essais[ligne-1, colonne-1] = result # Met ce résultat dans la grille essais du joueur
    joueur.stats["touche"] += 1 # Ajout aux stats du joueur un tir touché
    if result == C_legende["Coulé"]: # Si ce tir est un coulé
      joueur.stats["coule"] += 1# Ajout aux stats du joueur un bateau coulé
    cible.grille_bateaux[ligne-1, colonne-1] = 0 # Met un 0 dans la grille bateaux de la cible (plus de bateau flottant ici)
    return True # Il peut rejouer
def two_players(): 
  """Fait suivre le déroulement d'une partie composée de deux joueurs"""
  main = init(one_player=False) # Création de la partie
  pause()
  placement(main.j1) # Placement des bateaux du joueur 1
  pause()
  placement(main.j2) # Placement des bateaux du joueur 2
  pause()
  roulement(main) # Roulement des tours entre j1 et j2 jusqu'a fin de partie
  pause()
def one_player():
  """Fait suivre le déroulement d'une partie composée d'un seul joueur"""
  main = init(one_player=True) # Création de la partie
  pause()
  placement_alea(main.j2) # Placement aléatoire des bateaux de l'ordinateur
  pause()
  roulement_solo(main) # Roulement des essais de tir du joueur
  pause()

# Boucle Principale

print("-----Bienvenue dans la Bataille Navale----")
choix_valide=False
while not choix_valide: # Boucle principale du jeu avec menu principal
  choix=input("Voulez vous jouer à 1 ou 2 joueurs ? (Rentrez 1 ou 2):")
  if choix=="1":
    one_player() # Lancement déroulement partie 1 joueur
  elif choix=="2":
    two_players() # Lancement déroulement partie 2 joueurs
  else: # Si choix non valide
    print("Veuillez rentrer un choix valide")
    continue
  rejouer=input("Voulez vous rejouer (Oui ou Non) ? :")
  while rejouer.lower() != "oui" and rejouer.lower() != "non": # Si choix non valide
    print("Veuillez saisir une réponse valide")
    rejouer=input("Voulez vous rejouer (Oui ou Non) ? :")
  if rejouer.lower() == "non":
    choix_valide = True # Sortie de la boucle principale
    print("Passez une excellente journée :)")

    

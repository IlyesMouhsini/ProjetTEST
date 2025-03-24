from modele import *
from graphique import dessiner_map
from tkiteasy import ouvrirFenetre


#================================================
#============== FICHIER MAIN ====================
#================================================




# Dimensions de la fenêtre
LARGEUR = 718
HAUTEUR = 600

# carte du jeu
map_scenario = [
    "                        ",
    "                        ",
    "                        ",
    "CCCCCCCCCCCCCCCCCCCCCCCC",
    "C  P                   C",
    "CMCMCMCMC C CMC C C C  C", 
    "CM   M       M    MMM  C",
    "CMC CMC C C CMC C CMC  C",
    "C                  M   C",
    "C C C C C C CMC C C C  C",
    "C  MM    E  MMM        C",
    "C CMC C C C C C C C C  C",
    "C  M               MM  C",
    "C C C CMCMC C C C CMC  C",
    "C      MMM     E   M   C",
    "C CMCMC C C C C C C C  C",
    "C            M         C",
    "CMC C C C C CMC C C CMMC",
    "CMM         MMM      MMC",
    "CCCCCCCCCCCCCCCCCCCCCCCC"
]

def main():
    # Initialisation de la fenêtre graphique
    canvas = ouvrirFenetre(LARGEUR, HAUTEUR)

    # Accéder à la fenêtre principale (l'objet Tk)
    fenetre = canvas.master
    fenetre.title("BomberBUT")

    # Initialisation du jeu avec le canvas et la carte
    jeu = Jeu(canvas, map_scenario)

    # Fonction pour gérer les touches
    def on_key(event):
        jeu.handle_key(event.keysym)

    # Liaison des touches
    canvas.bind_all("<Key>", on_key)

    # Boucle principale
    canvas.mainloop()

if __name__ == "__main__":
    main()

#================================================
#================================================
#================================================
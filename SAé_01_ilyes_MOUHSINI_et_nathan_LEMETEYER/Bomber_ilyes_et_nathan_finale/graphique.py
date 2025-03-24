from tkiteasy import *

#=====================================================
#============== FICHIER GRAPHIQUE ====================
#=====================================================


TAILLE_CASE = 30  # Taille des cases pour l'affichage

def dessiner_map(canvas, map_data, taille_c):
    """
    Dessine la carte sur le canevas.
    :param canvas: Le canevas où dessiner.
    :param map_data: Les données de la carte (liste de chaînes).
    :param taille_c: La taille des cases en pixels.
    """
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            px, py = x * taille_c, y * taille_c
            color = {
                "C": "gray",    # Colonne indestructible
                "M": "brown",   # Mur destructible
                "E": "blue",    # Prise Ethernet
                "P": "green",   # Bomber
                "F": "red",     # Fantôme
                "U": "yellow",  # Upgrade
                "B": "white",   # Bombe
                " ": "black",   # Case vide
            }.get(cell, "black")
            canvas.dessinerRectangle(px, py, taille_c, taille_c, color)


#=====================================================
#=====================================================
#=====================================================
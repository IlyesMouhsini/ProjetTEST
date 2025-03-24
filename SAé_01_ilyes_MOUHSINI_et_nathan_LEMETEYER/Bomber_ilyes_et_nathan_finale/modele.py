import random
from graphique import dessiner_map




#==================================================
#============== FICHIER MODELE ====================
#==================================================



TAILLE_CASE = 30  # Taille des cases en pixels (mis ici car l'importation depuis le fichier graphique ne marchait pas)


# ===================================================================== #
# ========================== CLASSES ================================== #
# ===================================================================== #



# ============================== BOMBER ===============================

class Bomber:
    def __init__(self, x, y):
        """
        Initialise un Bomber à une position donnée avec un nombre de points de vie par défaut.
        :param x: Position x initiale.
        :param y: Position y initiale.
        """
        self.x = x
        self.y = y
        self.vie = 3  # Points de vie du Bomber

    def mouvements(self, direction, game):
        """
        Déplace le Bomber dans une direction donnée si la case cible n'est pas bloquante.
        :param direction: Direction du mouvement ("up", "down", "left", "right").
        :param game: Instance du jeu pour vérifier la validité du mouvement.
        """
        new_x, new_y = self.x, self.y
        if direction == "up":
            new_y -= 1
        elif direction == "down":
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1

        if game.non_bloquante(new_x, new_y):
            game.update_map(self.x, self.y, new_x, new_y)
            self.x, self.y = new_x, new_y

# ============================ FANTOME ================================

class Fantome:
    def __init__(self, x, y):
        """
        Initialise un Fantôme à une position donnée.
        """
        self.x = x
        self.y = y

    def move(self, game):
        """
        Déplace le Fantôme dans une direction aléatoire si la case cible est accessible.
        """
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)
        for direction in directions:
            new_x, new_y = self.x, self.y
            if direction == "up":
                new_y -= 1
            elif direction == "down":
                new_y += 1
            elif direction == "left":
                new_x -= 1
            elif direction == "right":
                new_x += 1
            if game.non_bloquante_for_fantome(new_x, new_y):
                self.x, self.y = new_x, new_y
                return

# ============================= JEU ====================================

class Jeu:
    def __init__(self, canvas, map_data):
        """
        Initialise une instance de jeu avec le canevas graphique et la carte donnée.
        """
        self.canvas = canvas
        self.map_data = [list(row) for row in map_data]
        self.bomber = self.trouve_bomber()
        self.bomber.vie = 3  # Réinitialise la vie du Bomber
        self.niveau = 0  # Niveau initial
        self.fantomes = []
        self.bombes = []  # Liste des bombes actives
        self.portée_explosion = 2  # Portée initiale des explosions
        self.nb_bombes_max = 1  # Nombre maximum de bombes posées simultanément
        self.upgrades = []  # Liste des upgrades sur la carte
        self.score = 0  # Score du Bomber
        self.timer_global = 500  # Durée totale du jeu en tours
        self.draw_map()
        self.tour = 0  # Compteur de tours
        self.fantome_timer = 10  # Intervalle en tours pour générer des fantômes

    def tour_de_jeu(self):
        """
        Gère un tour complet :
        - Gère le timer global.
        - Génère des fantômes tous les N tours.
        - Déplace les fantômes.
        - Met à jour les bombes.
        - Vérifie les interactions.
        """
        if self.bomber.vie <= 0:
            print("Fin de la partie détectée dans tour_de_jeu (le bomber n'a plus de vie).")
            self.fin_du_jeu()
            return

        # Timer global (le timer de la partie)
        self.timer_global -= 1
        if self.timer_global == 0:
            print(f"Fin du jeu ! Score final : {self.score}")
            self.canvas.fermerFenetre()
            return

        # Gestion du timer pour les fantômes
        if self.fantome_timer > 0:
            self.fantome_timer -= 1

        if self.fantome_timer == 0:
            self.generate_fantomes()
            self.fantome_timer = 10  # Réinitialise le compteur

        # Actions des fantômes, bombes et autres interactions
        self.move_fantomes()      # Déplace les fantômes
        self.update_bombes()      # Met à jour les bombes
        self.ramasser_upgrade()   # Vérifie les upgrades ramassés
        self.attack_bomber()      # Vérifie les attaques des fantômes
        self.tour += 1
        print(f"Tour : {self.tour}, Timer (nombre de tours restants) : {self.timer_global}")






    def trouve_bomber(self):
        """
        Trouve la position initiale du Bomber sur la carte.
        :return: Instance de Bomber si trouvée, sinon None.
        """
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == "P":
                    return Bomber(x, y)
        return None

    def non_bloquante(self, x, y):
        """
        Vérifie si une case est accessible pour le Bomber.
        :return: True si la case est accessible, False sinon.
        """
        return 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]) and self.map_data[y][x] in [" ", "U"]

    def update_map(self, old_x, old_y, new_x, new_y):
        """
        Met à jour la carte après un déplacement du Bomber.
        :param old_x: Ancienne position x du Bomber.
        :param old_y: Ancienne position y du Bomber.
        :param new_x: Nouvelle position x du Bomber.
        :param new_y: Nouvelle position y du Bomber.
        """
        self.map_data[old_y][old_x] = " "
        self.map_data[new_y][new_x] = "P"
        self.update_case(old_x, old_y)
        self.update_case(new_x, new_y)

    def update_case(self, x, y):
        """
        Met à jour visuellement une case spécifique.
        """
        cell = self.map_data[y][x]
        px, py = x * TAILLE_CASE, y * TAILLE_CASE
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
        self.canvas.dessinerRectangle(px, py, TAILLE_CASE, TAILLE_CASE, color)


    def draw_map(self):
        dessiner_map(self.canvas, self.map_data, TAILLE_CASE)  # Passe les 3 arguments requis


    def generate_fantomes(self):
        """
        Génère des fantômes autour de chaque prise Ethernet ('E'), avec une limite globale de fantômes.
        """
        MAX_FANTOMES = 8  # Limite maximale de fantômes dans le jeu
        if len(self.fantomes) >= MAX_FANTOMES:
            return  # Ne rien faire si la limite est atteinte

        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == "E":  # Trouve une prise Ethernet
                    # Vérifie si on peut encore générer des fantômes
                    if len(self.fantomes) >= MAX_FANTOMES:
                        break

                    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                    random.shuffle(directions)  # Mélange les directions
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if self.non_bloquante_for_fantome(nx, ny):
                            # Crée un nouveau fantôme
                            self.fantomes.append(Fantome(nx, ny))
                            self.map_data[ny][nx] = "F"  # Place le fantôme sur la carte
                            self.update_case(nx, ny)    # Redessine la case
                            print(f"Fantôme généré à ({nx}, {ny})")
                            break  # Passe au générateur suivant



    def non_bloquante_for_fantome(self, x, y):
        """
        Vérifie si une case est accessible pour un Fantôme.
        :param x: Coordonnée x de la case.
        :param y: Coordonnée y de la case.
        :return: True si la case est accessible, False sinon.
        """ 
        return 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]) and self.map_data[y][x] == " "

    def move_fantomes(self):
        """
        Déplace tous les fantômes et met à jour leurs cases.
        """
        for fantome in self.fantomes:
            old_x, old_y = fantome.x, fantome.y
            fantome.move(self)
            if (fantome.x, fantome.y) != (old_x, old_y):
                self.map_data[old_y][old_x] = " "
                self.map_data[fantome.y][fantome.x] = "F"
                self.update_case(old_x, old_y)
                self.update_case(fantome.x, fantome.y)

    def attack_bomber(self):
        """
        Vérifie si un Fantôme attaque le Bomber.
        Réduit les points de vie du Bomber si un Fantôme est adjacent (distance de Manhattan = 1).
        Si les points de vie du Bomber tombent à 0 ou moins, termine la partie.
        """
        for fantome in self.fantomes:
            if abs(fantome.x - self.bomber.x) + abs(fantome.y - self.bomber.y) == 1:
                self.bomber.vie -= 1
                print(f"Le Bomber a été attaqué ! Points de vie restants : {self.bomber.vie}")
                if self.bomber.vie <= 0:
                    print("Le Bomber a perdu toutes ses vies. Fin de la partie.")
                    self.fin_du_jeu()
                    return  # Stoppe l'exécution de cette méthode


    
    def handle_key(self, key):
        """
        Gère les actions du joueur, puis passe au tour suivant.
        """
        if key == "Up":
            self.bomber.mouvements("up", self)
        elif key == "Down":
            self.bomber.mouvements("down", self)
        elif key == "Left":
            self.bomber.mouvements("left", self)
        elif key == "Right":
            self.bomber.mouvements("right", self)
        elif key == "space":  # Touche pour poser une bombe
            self.poser_bombe()
        self.ramasser_upgrade()  # Vérifie si un upgrade est ramassé
        self.tour_de_jeu()




    def poser_bombe(self):
        """
        Pose une bombe à la position du Bomber si possible.
        """
        if len(self.bombes) < self.nb_bombes_max:
            x, y = self.bomber.x, self.bomber.y
            self.bombes.append(Bombe(x, y, self.portée_explosion, tours_avant_explosion=5))
            self.map_data[y][x] = "B"  # Marque la bombe sur la carte
            self.update_case(x, y)  # Redessine la case


    def exploser_bombe(self, bombe):
        """
        Gère l'explosion d'une bombe.
        """
        x, y = bombe.x, bombe.y
        self.map_data[y][x] = " "  # Retire la bombe de la carte
        self.update_case(x, y)

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Haut, bas, gauche, droite
        for dx, dy in directions:
            for i in range(1, bombe.portée + 1):
                nx, ny = x + dx * i, y + dy * i
                if not (0 <= ny < len(self.map_data) and 0 <= nx < len(self.map_data[0])):
                    break  # Hors de la carte

                case = self.map_data[ny][nx]
                if case == "C":  # Colonne indestructible bloque l'explosion
                    break
                elif case == "M":  # Mur destructible
                    self.map_data[ny][nx] = " "  # Détruit le mur
                    self.update_case(nx, ny)
                    self.score += 1  # Le Bomber marque 1 point
                    break
                elif case == "F":  # Fantôme
                    self.fantomes = [f for f in self.fantomes if not (f.x == nx and f.y == ny)]
                    self.map_data[ny][nx] = "U"  # Place un upgrade
                    self.update_case(nx, ny)
                    print(f"Fantôme détruit à ({nx}, {ny}). Upgrade placé.")  # Débogage
                    break

                elif case == "P":  # Bomber
                    self.bomber.vie -= 1
                    print(f"Le Bomber a été touché ! Vie restante : {self.bomber.vie}")
                    break
                elif case == "U":  # Upgrade
                    self.map_data[ny][nx] = " "  # Détruit l'upgrade
                    self.update_case(nx, ny)
                    break
                elif case == "B":  # Autre bombe
                    # Explosion en chaîne
                    bombe_chainee = next((b for b in self.bombes if b.x == nx and b.y == ny), None)
                    if bombe_chainee:
                        self.exploser_bombe(bombe_chainee)

                # Marquer temporairement l'explosion
                self.map_data[ny][nx] = "X"  # Explosion visible
                self.update_case(nx, ny)

        # Nettoyer les explosions après un tour
        self.clean_explosions()




    def clean_explosions(self):
        """
        Supprime les marqueurs d'explosion ('X') après un tour.
        """
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == "X":
                    self.map_data[y][x] = " "  # Remet la case à vide
                    self.update_case(x, y)
    

    
    def update_bombes(self):
        """
        Met à jour les bombes, les fait exploser si leur délai est écoulé.
        """
        bombes_restantes = []
        for bombe in self.bombes:
            if bombe.tick():
                self.exploser_bombe(bombe)  # Explosion différée
            else:
                # Met à jour la carte pour s'assurer que la bombe reste visible
                self.map_data[bombe.y][bombe.x] = "B"
                self.update_case(bombe.x, bombe.y)
                bombes_restantes.append(bombe)
        self.bombes = bombes_restantes




    def placer_upgrade(self, x, y, type_upgrade):
        """
        Place un upgrade sur la carte.
        """
        self.upgrades.append((x, y, type_upgrade))
        self.map_data[y][x] = "U"  # Marque l'upgrade sur la carte
        self.update_case(x, y)

    def ramasser_upgrade(self):
        """
        Vérifie si le Bomber ramasse un upgrade et applique les effets.
        """

        x, y = self.bomber.x, self.bomber.y
        if self.map_data[y][x] == "U":  # Vérifie si la case contient un upgrade
            self.map_data[y][x] = " "  # Supprime l'upgrade de la carte
            self.update_case(x, y)  # Met à jour l'affichage
            self.bomber.niveau += 1  # Augmente le niveau du Bomber
            self.score += 3  # Le Bomber marque 3 points
            print(f"Upgrade ramassé ! Niveau actuel : {self.bomber.niveau}, Score : {self.score}")

            # Applique les effets du niveau
            if self.bomber.niveau % 2 == 1:  # Niveau impair : +1 PV
                self.bomber.vie += 1
                print(f"Le Bomber gagne 1 PV. Vie actuelle : {self.bomber.vie}")
            elif self.bomber.niveau % 2 == 0:  # Niveau pair : +1 portée
                self.portée_explosion += 1
                print(f"Portée augmentée. Portée actuelle : {self.portée_explosion}")



    def fin_du_jeu(self):
        """
        Gère la fin du jeu.
        """
        print(f"Fin du jeu ! Score final : {self.score}")
        self.canvas.fermerFenetre()



# ============================= BOMBES ==========================================

class Bombe:
    def __init__(self, x, y, portée, tours_avant_explosion):
        self.x = x
        self.y = y
        self.portée = portée
        self.tours_restants = tours_avant_explosion

    def tick(self):
        """
        Réduit le nombre de tours restants avant l'explosion.
        """
        self.tours_restants -= 1
        return self.tours_restants <= 0  # Retourne True si la bombe doit exploser
    



# ===================================================================== #
# ===================================================================== #
# ===================================================================== #
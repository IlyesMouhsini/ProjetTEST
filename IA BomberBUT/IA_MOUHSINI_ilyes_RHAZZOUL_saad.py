import random

class IA_Bomber:
    def __init__(self, num_joueur: int, game_dic: dict, timerglobal: int, timerfantôme: int) -> None:
        """Initialise l'IA avec ses paramètres de base.
        
        Args:
            num_joueur (int): Numéro identifiant le joueur
            game_dic (dict): État initial du jeu
            timerglobal (int): Temps total de la partie
            timerfantôme (int): Temps d'invincibilité
        """
        self.num_joueur = num_joueur
        self.game_dic = game_dic
        self.timerglobal = timerglobal
        self.timerfantôme = timerfantôme
        self.chemin = []
        self.positions_visitees = set()
        self.derniere_bombe = None
        self.compteur_blocage = 0

    def trouver_chemin(self, debut: tuple, fin: tuple, carte: list) -> list:
        """Trouve le plus court chemin entre deux points en utilisant BFS.
        
        Args:
            debut (tuple): Position de départ (x, y)
            fin (tuple): Position d'arrivée (x, y)
            carte (list): Carte du jeu

        Returns:
            list: Liste des directions ['H', 'B', 'G', 'D'] ou None si pas de chemin
        """
        if debut == fin:
            return []
        
        # Initialisation de la recherche
        queue = [(debut, [])]
        visites = {debut}
        
        # Parcours en largeur (BFS)
        while queue:
            (x, y), chemin = queue.pop(0)
            
            # Test des 4 directions possibles
            for dx, dy, direction in [(0, -1, 'H'), (0, 1, 'B'), (-1, 0, 'G'), (1, 0, 'D')]:
                nouveau_x, nouveau_y = x + dx, y + dy
                
                # Si on a trouvé la destination
                if (nouveau_x, nouveau_y) == fin:
                    return chemin + [direction]
                    
                # Si la case est valide et non visitée
                if (0 <= nouveau_x < len(carte[0]) and 
                    0 <= nouveau_y < len(carte) and 
                    carte[nouveau_y][nouveau_x] != 'C' and 
                    (nouveau_x, nouveau_y) not in visites):
                    queue.append(((nouveau_x, nouveau_y), chemin + [direction]))
                    visites.add((nouveau_x, nouveau_y))
        return None

    def est_pres_bombe(self, x: int, y: int, game_dict: dict) -> bool:
        """Vérifie si une position est dans la zone de danger d'une bombe.
        
        Args:
            x (int): Coordonnée x de la position
            y (int): Coordonnée y de la position
            game_dict (dict): État actuel du jeu

        Returns:
            bool: True si la position est en danger, False sinon
        """
        for bombe in game_dict['bombes']:
            bx, by = bombe['position']
            # Portée de 2 cases (portée réelle des bombes)
            if abs(x - bx) + abs(y - by) <= 2:
                return True
        return False

    def trouver_minerai_proche(self, game_dict: dict) -> tuple:
        """Trouve le minerai le plus proche et accessible.
        
        Args:
            game_dict (dict): État actuel du jeu

        Returns:
            tuple: Coordonnées (x, y) du minerai le plus proche ou None si aucun
        """
        carte = game_dict['map']
        pos = game_dict['bombers'][self.num_joueur]['position']
        x, y = pos
        
        # Liste des minerais accessibles avec leur distance
        minerais = []
        for i in range(len(carte)):
            for j in range(len(carte[0])):
                if carte[i][j] == 'M':
                    chemin = self.trouver_chemin((x, y), (j, i), carte)
                    if chemin:
                        minerais.append(((j, i), len(chemin)))
        
        # Retourne le minerai le plus proche
        if minerais:
            return min(minerais, key=lambda x: x[1])[0]
        return None

    def action(self, game_dict: dict) -> str:
        """Décide de la prochaine action à effectuer.
        
        Args:
            game_dict (dict): État actuel du jeu

        Returns:
            str: Action à effectuer ('H', 'B', 'G', 'D', 'X' ou 'N')
        """
        pos_actuelle = game_dict['bombers'][self.num_joueur]['position']
        x, y = pos_actuelle
        carte = game_dict['map']

        # PRIORITÉ 1 : Sécurité - S'éloigner des bombes
        if self.est_pres_bombe(x, y, game_dict):
            # Essaie de reculer de 2 cases si possible
            if x > 1 and carte[y][x-1] != 'C' and carte[y][x-2] != 'C':
                return 'G'
            if y > 1 and carte[y-1][x] != 'C' and carte[y-2][x] != 'C':
                return 'H'
            # Sinon recule d'une case
            if x > 0 and carte[y][x-1] != 'C':
                return 'G'
            if y > 0 and carte[y-1][x] != 'C':
                return 'H'
            return 'N'

        # PRIORITÉ 2 : Attendre que les bombes explosent
        if game_dict['bombes']:
            return 'N'

        # PRIORITÉ 3 : Chercher et détruire les minerais
        minerai = self.trouver_minerai_proche(game_dict)
        if minerai:
            minerai_x, minerai_y = minerai

            # Si adjacent au minerai, pose une bombe
            if abs(x - minerai_x) + abs(y - minerai_y) == 1:
                self.derniere_bombe = (x, y)
                return 'X'

            # Sinon se déplace vers le minerai
            chemin = self.trouver_chemin((x, y), (minerai_x, minerai_y), carte)
            if chemin:
                return chemin[0]

        # PRIORITÉ 4 : Gestion du blocage
        if pos_actuelle in self.positions_visitees:
            self.compteur_blocage += 1
            if self.compteur_blocage > 3:
                self.positions_visitees.clear()
                self.compteur_blocage = 0
                return 'X'
        else:
            self.positions_visitees.add(pos_actuelle)
            self.compteur_blocage = 0

        # Si aucune action n'est possible
        return 'N'
#! /usr/bin/env python3
"""Parcours à la volée de l'arbre de calculs du compte est bon.

Un état contient les valeurs encore utilisables et leur expression NPI. Les
résultats intermédiaires sont strictement positifs et les divisions exactes.
"""

from TAD.piles_listes_python import Pile
from TAD.files_listes_doublement_chainees import File


def _operations(a, b, expression_a, expression_b):
    """Les six opérations possibles ; None représente un calcul invalide."""
    yield a + b, expression_a + expression_b + ['+']
    yield a * b, expression_a + expression_b + ['*']
    yield ((a - b, expression_a + expression_b + ['-']) if a > b else None)
    yield ((b - a, expression_b + expression_a + ['-']) if b > a else None)
    yield ((a // b, expression_a + expression_b + ['/'])
           if b and a % b == 0 else None)
    yield ((b // a, expression_b + expression_a + ['/'])
           if a and b % a == 0 else None)


def _successeurs(etat):
    for i in range(len(etat)):
        for j in range(i + 1, len(etat)):
            a, expression_a = etat[i]
            b, expression_b = etat[j]
            restants = [element for k, element in enumerate(etat) if k not in (i, j)]
            for operation in _operations(a, b, expression_a, expression_b):
                yield operation, restants


def _contexte(cartons, cible, stats):
    if not cartons:
        raise ValueError('Il faut au moins un carton')
    if any(not isinstance(c, int) or c <= 0 for c in cartons):
        raise ValueError('Les cartons doivent être des entiers strictement positifs')
    if stats is None:
        stats = {}
    stats.clear()
    stats.update(noeuds=1, invalides=0, redondants=0, etats_uniques=1,
                 hauteur_max=0, largeur_max=1, frontiere_max=0)
    etat = [(carton, [carton]) for carton in cartons]
    vus = {tuple(sorted(cartons))}
    largeurs = [1] + [0] * (len(cartons) - 1)
    meilleur = [float('inf'), []]

    def examiner(valeur, expression):
        distance = abs(cible - valeur)
        if distance < meilleur[0]:
            meilleur[:] = [distance, expression]
            print(' '.join(map(str, expression)), '=', valeur)
        return valeur == cible

    for valeur, expression in etat:
        if examiner(valeur, expression):
            return stats, etat, vus, largeurs, meilleur, examiner, True
    return stats, etat, vus, largeurs, meilleur, examiner, False


def _nouveau_etat(operation, restants, profondeur, stats, vus, largeurs, examiner):
    """Compte un calcul tenté, puis conserve seulement les états distincts."""
    stats['noeuds'] += 1
    if operation is None:
        stats['invalides'] += 1
        return None, False
    valeur, expression = operation
    trouve = examiner(valeur, expression)
    nouvel_etat = restants + [(valeur, expression)]
    signature = tuple(sorted(v for v, _ in nouvel_etat))
    if signature in vus:
        stats['redondants'] += 1
        return None, trouve
    vus.add(signature)
    stats['etats_uniques'] += 1
    largeurs[profondeur] += 1
    stats['largeur_max'] = max(stats['largeur_max'], largeurs[profondeur])
    stats['hauteur_max'] = max(stats['hauteur_max'], profondeur)
    return nouvel_etat, trouve


def parcours_DFS(cartons, cible, stats=None):
    """DFS itératif : pile de cadres (un itérateur de fils par niveau)."""
    stats, initial, vus, largeurs, meilleur, examiner, trouve = _contexte(cartons, cible, stats)
    if trouve:
        return stats['noeuds'], meilleur[1]
    pile = Pile()
    pile.empiler((_successeurs(initial), 0))
    stats['frontiere_max'] = 1
    while not pile.est_vide():
        successeurs, profondeur = pile.sommet()
        try:
            operation, restants = next(successeurs)
        except StopIteration:
            pile.depiler()
            continue
        enfant, atteint = _nouveau_etat(operation, restants, profondeur + 1,
                                        stats, vus, largeurs, examiner)
        if atteint:
            return stats['noeuds'], meilleur[1]
        if enfant is not None:
            pile.empiler((_successeurs(enfant), profondeur + 1))
            stats['frontiere_max'] = max(stats['frontiere_max'], pile.longueur())
    return stats['noeuds'], meilleur[1]


def parcours_BFS(cartons, cible, stats=None):
    """BFS itératif : renvoie (calculs examinés, meilleure expression NPI)."""
    stats, initial, vus, largeurs, meilleur, examiner, trouve = _contexte(cartons, cible, stats)
    if trouve:
        return stats['noeuds'], meilleur[1]
    frontiere = File()
    frontiere.enfiler((initial, 0))
    stats['frontiere_max'] = 1
    taille = 1
    while taille:
        etat, profondeur = frontiere.defiler()
        taille -= 1
        for operation, restants in _successeurs(etat):
            enfant, trouve = _nouveau_etat(operation, restants, profondeur + 1,
                                          stats, vus, largeurs, examiner)
            if trouve:
                return stats['noeuds'], meilleur[1]
            if enfant is not None:
                frontiere.enfiler((enfant, profondeur + 1))
                taille += 1
                stats['frontiere_max'] = max(stats['frontiere_max'], taille)
    return stats['noeuds'], meilleur[1]


def parcours_DFS_recursif(cartons, cible, stats=None):
    """DFS récursif : même contrat, profondeur bornée au nombre de cartons."""
    stats, initial, vus, largeurs, meilleur, examiner, trouve = _contexte(cartons, cible, stats)
    if trouve:
        return stats['noeuds'], meilleur[1]
    stats['frontiere_max'] = 1

    def visiter(etat, profondeur):
        for operation, restants in _successeurs(etat):
            enfant, atteint = _nouveau_etat(operation, restants, profondeur + 1,
                                            stats, vus, largeurs, examiner)
            if atteint:
                return True
            if enfant is not None:
                stats['frontiere_max'] = max(stats['frontiere_max'], profondeur + 2)
                if visiter(enfant, profondeur + 1):
                    return True
        return False

    visiter(initial, 0)
    return stats['noeuds'], meilleur[1]


if __name__ == '__main__':
    for recherche in (parcours_DFS, parcours_DFS_recursif, parcours_BFS):
        print(recherche.__name__, recherche([3, 5, 7, 9, 25, 50], 859))

#! /usr/bin/env python3

"""
Ce programme prendra sur son entrée standard les 6 cartons tirés au sort suivis du nombre à
trouver. Par exemple, si les cartons tirés sont 3 5 7 9 25 50 et que le nombre à découvrir est
859, il devra être appelé ainsi : echo 3 5 7 9 25 50 859  | ./compteestbon.py 
"""

from recherche_compte_est_bon import parcours_DFS, parcours_DFS_recursif, parcours_BFS
from notation_polonaise_inverse import eval_NPI_liste
import sys
import time

def lire_stdin():
    """Lit l'entrée standard en invitant l'utilisateur à l'aide d'un message si le flux d'entrée n'est pas redirigé"""
    if sys.stdin.isatty():
        sys.stderr.write("Saisissez du texte (Ctrl+D pour terminer) :\n")
    return sys.stdin.read()

if __name__ == "__main__":
    cartons_nombre = lire_stdin()
    try:
        *cartons, nombre = map(int, cartons_nombre.split())
        if not cartons:
            raise ValueError('aucun carton')
    except ValueError:
        sys.exit('Entrée invalide : fournir les six cartons (ou au moins un carton) '
                 'puis la cible, en entiers séparés par des espaces.')
    print(f"Recherche de {nombre} avec {cartons}")
    
    for nom, parcours in (("DFS", parcours_DFS),
                         ("DFS récursif", parcours_DFS_recursif),
                         ("BFS", parcours_BFS)):
        statistiques = {}
        debut = time.perf_counter()
        noeuds, expression = parcours(cartons, nombre, stats=statistiques)
        duree = time.perf_counter() - debut
        _, valeur = eval_NPI_liste(expression)
        print(f"{nom} : {duree:.6f} s | Nœuds : {noeuds} | "
              f"Hauteur max : {statistiques['hauteur_max']} | "
              f"Largeur max : {statistiques['largeur_max']} | "
              f"{'File' if nom == 'BFS' else 'Pile'} max : {statistiques['frontiere_max']} | "
              f"Meilleur résultat : {valeur} | NPI : {expression}")
    

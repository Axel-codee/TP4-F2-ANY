#! /usr/bin/env python3
"""Mesures reproductibles du TP4 : python experimentation_tp4.py [répétitions]."""

import contextlib
import io
import statistics
import subprocess
import sys
import time

from generer_probleme import ARDUS, IMPOSSIBLES
from notation_polonaise_inverse import eval_NPI_liste
from recherche_compte_est_bon import parcours_BFS, parcours_DFS, parcours_DFS_recursif


def problemes():
    # La graine du README est un exemple, pas la date de naissance de l'étudiant.
    sortie = subprocess.check_output([sys.executable, 'generer_probleme.py', '17081936'],
                                     text=True)
    *cartons, cible = map(int, sortie.split())
    return (('17081936', cartons, cible),
            ('impossible', IMPOSSIBLES[0][:-1], IMPOSSIBLES[0][-1]),
            ('ardu', ARDUS[0][:-1], ARDUS[0][-1]))


def mesurer(repetitions=5):
    if repetitions < 1:
        raise ValueError('Nombre de répétitions strictement positif attendu')
    print('| Cas | Tirage → cible | Parcours | Nœuds | Invalides | Redondants | '
          'États uniques | Pile/file max | Hauteur | Largeur | Résultat | Temps médian (ms) |')
    print('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for nom, cartons, cible in problemes():
        for parcours, etiquette in ((parcours_DFS, 'DFS'),
                                    (parcours_DFS_recursif, 'DFS récursif'),
                                    (parcours_BFS, 'BFS')):
            mesures = []
            stats = {}
            noeuds, valeur = 0, None
            for _ in range(repetitions):
                stats = {}
                with contextlib.redirect_stdout(io.StringIO()):
                    debut = time.perf_counter()
                    noeuds, expression = parcours(cartons, cible, stats=stats)
                    mesures.append((time.perf_counter() - debut) * 1000)
                valide, valeur = eval_NPI_liste(expression)
                assert valide and valeur is not None
            tirage = ' '.join(map(str, cartons)) + ' → ' + str(cible)
            print(f'| {nom} | {tirage} | {etiquette} | {noeuds} | '
                  f"{stats['invalides']} | {stats['redondants']} | "
                  f"{stats['etats_uniques']} | {stats['frontiere_max']} | "
                  f"{stats['hauteur_max']} | {stats['largeur_max']} | "
                  f'{valeur} | {statistics.median(mesures):.3f} |', flush=True)


if __name__ == '__main__':
    mesurer(int(sys.argv[1]) if len(sys.argv) > 1 else 5)

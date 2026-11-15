"""Tests de comportement des trois parcours du TP4."""

import contextlib
import io
import subprocess
import sys
import unittest

from notation_polonaise_inverse import eval_NPI_liste
from recherche_compte_est_bon import parcours_BFS, parcours_DFS, parcours_DFS_recursif


PARCOURS = (parcours_DFS, parcours_DFS_recursif, parcours_BFS)


class TestParcours(unittest.TestCase):
    def test_experimentation_reproductible(self):
        execution = subprocess.run([sys.executable, 'experimentation_tp4.py', '1'],
                                   text=True, capture_output=True, check=True)
        self.assertIn('17081936', execution.stdout)
        self.assertIn('impossible', execution.stdout)
        self.assertIn('ardu', execution.stdout)
        self.assertEqual(execution.stdout.count('| DFS |'), 3)
        self.assertEqual(execution.stdout.count('| BFS |'), 3)

    def test_programme_affiche_resultats_et_mesures(self):
        execution = subprocess.run([sys.executable, 'compte_est_bon.py'],
                                   input='2 3 5\n', text=True, capture_output=True, check=True)
        for nom in ('DFS', 'DFS récursif', 'BFS'):
            self.assertIn(f'{nom} :', execution.stdout)
        self.assertIn('Nœuds : 2', execution.stdout)
        self.assertIn('Hauteur max : 1', execution.stdout)

    def test_entree_vide_affiche_un_message_sans_traceback(self):
        execution = subprocess.run([sys.executable, 'compte_est_bon.py'],
                                   input='', text=True, capture_output=True)
        self.assertNotEqual(execution.returncode, 0)
        self.assertIn('six cartons', execution.stderr)
        self.assertNotIn('Traceback', execution.stderr)

    def executer(self, parcours, cartons, cible):
        statistiques = {}
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            resultat = parcours(cartons, cible, stats=statistiques)
        return resultat, statistiques, sortie.getvalue()

    def test_solution_directe_et_comptage_precis(self):
        for parcours in PARCOURS:
            with self.subTest(parcours=parcours.__name__):
                (noeuds, expression), stats, sortie = self.executer(parcours, [2, 3], 5)
                self.assertEqual(noeuds, 2)  # Racine et première opération examinée.
                self.assertEqual(eval_NPI_liste(expression), (True, 5))
                self.assertEqual(stats['noeuds'], noeuds)
                self.assertEqual(stats['hauteur_max'], 1)
                self.assertEqual(stats['largeur_max'], 1)
                self.assertEqual(stats['frontiere_max'], 1)
                self.assertIn('= 5', sortie)

    def test_carton_seul_et_arret_immediat(self):
        for parcours in PARCOURS:
            with self.subTest(parcours=parcours.__name__):
                (noeuds, expression), stats, _ = self.executer(parcours, [3, 5, 7], 5)
                self.assertEqual((noeuds, expression), (1, [5]))
                self.assertEqual(stats['hauteur_max'], 0)
                self.assertEqual(stats['frontiere_max'], 0)

    def test_impossible_retourne_le_plus_proche_et_ignore_operations_invalides(self):
        for parcours in PARCOURS:
            with self.subTest(parcours=parcours.__name__):
                (noeuds, expression), stats, sortie = self.executer(parcours, [2, 3], 4)
                valide, valeur = eval_NPI_liste(expression)
                self.assertTrue(valide)
                self.assertEqual(abs(4 - valeur), 1)
                self.assertEqual(noeuds, 7)  # Racine + 6 opérations possibles.
                self.assertEqual(stats['invalides'], 3)  # Soustraction négative et deux divisions.
                self.assertEqual(stats['largeur_max'], 3)  # 5, 6 et 1.
                self.assertEqual(stats['hauteur_max'], 1)
                self.assertEqual(stats['etats_uniques'], 4)
                self.assertTrue(sortie)

    def test_expression_npi_utilise_les_cartons_au_plus_une_fois(self):
        for parcours in PARCOURS:
            with self.subTest(parcours=parcours.__name__):
                (_, expression), _, _ = self.executer(parcours, [2, 3, 4], 12)
                self.assertEqual(eval_NPI_liste(expression), (True, 12))
                nombres = [terme for terme in expression if isinstance(terme, int)]
                self.assertEqual(len(nombres), len(set(nombres)))
                self.assertTrue(set(nombres) <= {2, 3, 4})

    def test_dfs_iteratif_et_recursif_ont_le_meme_ordre(self):
        resultat_iteratif, _, sortie_iterative = self.executer(parcours_DFS, [2, 3, 4, 5], 10)
        resultat_recursif, _, sortie_recursive = self.executer(parcours_DFS_recursif, [2, 3, 4, 5], 10)
        self.assertEqual(resultat_iteratif, resultat_recursif)
        self.assertEqual(sortie_iterative, sortie_recursive)

    def test_bfs_trouve_une_solution_en_moins_d_operations(self):
        (_, expression_dfs), _, _ = self.executer(parcours_DFS, [2, 3, 4, 5], 10)
        (_, expression_bfs), _, _ = self.executer(parcours_BFS, [2, 3, 4, 5], 10)
        self.assertEqual(eval_NPI_liste(expression_dfs), (True, 10))
        self.assertEqual(eval_NPI_liste(expression_bfs), (True, 10))
        self.assertEqual(len(expression_bfs), 3)  # 2 5 *
        self.assertGreater(len(expression_dfs), len(expression_bfs))

    def test_entree_non_modifiee(self):
        cartons = [2, 2, 3]
        for parcours in PARCOURS:
            self.executer(parcours, cartons, 7)
        self.assertEqual(cartons, [2, 2, 3])


if __name__ == '__main__':
    unittest.main()

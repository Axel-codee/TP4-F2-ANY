#! /usr/bin/env python3

""" Implémentation des parcours de l’arbre de calculs à la volée :
- parcours en profondeur d’abord itératif
- parcours en profondeur d’abord récursif
- parcours en largeur d’abord itératif """

#from TAD.piles_listes_python import Pile
#from TAD.files_listes_python import File
#from TAD.piles_listes_simplement_chainees import Pile
#from TAD.files_listes_doublement_chainees import File
from notation_polonaise_inverse import *

def parcours_DFS(cartons, cible) : 
    # cartons : une liste
    # cible : entier 
    nb_noeuds = 0
    meilleure_expression = []
    meilleure_distance = float("inf")
    pile = Pile()
    etat_initial = [(carton, [carton]) for carton in cartons]
    pile.empiler(etat_initial)
    etats_vus = {tuple(sorted(cartons))}

    while not pile.est_vide():
        etat = pile.depiler()

        for valeur, expression in etat:
            distance = abs(cible - valeur)
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleure_expression = expression
                print(" ".join(map(str, expression)), "=", valeur)
                if valeur == cible:
                    return meilleure_expression, nb_noeuds

        for i in range(len(etat)):
            for j in range(i + 1, len(etat)):
                valeur_a, expression_a = etat[i]
                valeur_b, expression_b = etat[j]
                restants = [
                    element for k, element in enumerate(etat)
                    if k != i and k != j
                ]

                operations = [
                    (valeur_a + valeur_b, expression_a + expression_b + ["+"]),
                    (valeur_a * valeur_b, expression_a + expression_b + ["*"]),
                ]
                if valeur_a > valeur_b:
                    operations.append((valeur_a - valeur_b, expression_a + expression_b + ["-"]))
                if valeur_b > valeur_a:
                    operations.append((valeur_b - valeur_a, expression_b + expression_a + ["-"]))
                if valeur_b != 0 and valeur_a % valeur_b == 0:
                    operations.append((valeur_a // valeur_b, expression_a + expression_b + ["/"]))
                if valeur_a != 0 and valeur_b % valeur_a == 0:
                    operations.append((valeur_b // valeur_a, expression_b + expression_a + ["/"]))

                nb_noeuds += 6
                for nouvelle_valeur, nouvelle_expression in operations:
                    if nouvelle_valeur == cible:
                        print(" ".join(map(str, nouvelle_expression)), "=", nouvelle_valeur)
                        return nouvelle_expression, nb_noeuds

                    distance = abs(cible - nouvelle_valeur)
                    if distance < meilleure_distance:
                        meilleure_distance = distance
                        meilleure_expression = nouvelle_expression
                        print(" ".join(map(str, nouvelle_expression)), "=", nouvelle_valeur)

                    nouvel_etat = restants + [(nouvelle_valeur, nouvelle_expression)]
                    signature = tuple(sorted(valeur for valeur, _ in nouvel_etat))
                    if signature not in etats_vus:
                        etats_vus.add(signature)
                        pile.empiler(nouvel_etat)

    return meilleure_expression, nb_noeuds

def parcours_BFS(cartons, cible) : 
    # cartons : une liste
    # cible : entier 
    nb_noeuds = 0
    meilleure_expression = []
    meilleure_distance = float("inf")
    file = File()
    etat_initial = [(carton, [carton]) for carton in cartons]
    file.enfiler(etat_initial)
    etats_vus = {tuple(sorted(cartons))}

    while not file.est_vide():
        etat = file.defiler()

        for valeur, expression in etat:
            distance = abs(cible - valeur)
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleure_expression = expression
                print(" ".join(map(str, expression)), "=", valeur)
                if valeur == cible:
                    return meilleure_expression, nb_noeuds

        for i in range(len(etat)):
            for j in range(i + 1, len(etat)):
                valeur_a, expression_a = etat[i]
                valeur_b, expression_b = etat[j]
                restants = [
                    element for k, element in enumerate(etat)
                    if k != i and k != j
                ]

                operations = [
                    (valeur_a + valeur_b, expression_a + expression_b + ["+"]),
                    (valeur_a * valeur_b, expression_a + expression_b + ["*"]),
                ]
                if valeur_a > valeur_b:
                    operations.append((valeur_a - valeur_b, expression_a + expression_b + ["-"]))
                if valeur_b > valeur_a:
                    operations.append((valeur_b - valeur_a, expression_b + expression_a + ["-"]))
                if valeur_b != 0 and valeur_a % valeur_b == 0:
                    operations.append((valeur_a // valeur_b, expression_a + expression_b + ["/"]))
                if valeur_a != 0 and valeur_b % valeur_a == 0:
                    operations.append((valeur_b // valeur_a, expression_b + expression_a + ["/"]))

                nb_noeuds += 6
                for nouvelle_valeur, nouvelle_expression in operations:
                    if nouvelle_valeur == cible:
                        print(" ".join(map(str, nouvelle_expression)), "=", nouvelle_valeur)
                        return nouvelle_expression, nb_noeuds

                    distance = abs(cible - nouvelle_valeur)
                    if distance < meilleure_distance:
                        meilleure_distance = distance
                        meilleure_expression = nouvelle_expression
                        print(" ".join(map(str, nouvelle_expression)), "=", nouvelle_valeur)

                    nouvel_etat = restants + [(nouvelle_valeur, nouvelle_expression)]
                    signature = tuple(sorted(valeur for valeur, _ in nouvel_etat))
                    if signature not in etats_vus:
                        etats_vus.add(signature)
                        file.enfiler(nouvel_etat)

    return meilleure_expression, nb_noeuds 

def parcours_DFS_recursif(cartons, cible) :
    meilleure_expression = []
    nb_noeuds = 0
    meilleure_distance = float("inf")
    etats_vus = {tuple(sorted(cartons))}

    def parcours_DFSR_aux(etat):
        nonlocal meilleure_expression, meilleure_distance, nb_noeuds

        for valeur, expression in etat:
            distance = abs(cible - valeur)
            if distance < meilleure_distance:
                meilleure_distance = distance
                meilleure_expression = expression
                print(" ".join(map(str, expression)), "=", valeur)
                if valeur == cible:
                    return True

        for i in range(len(etat)):
            for j in range(i + 1, len(etat)):
                valeur_a, expression_a = etat[i]
                valeur_b, expression_b = etat[j]
                restants = [
                    element for k, element in enumerate(etat)
                    if k != i and k != j
                ]

                operations = [
                    (valeur_a + valeur_b, expression_a + expression_b + ["+"]),
                    (valeur_a * valeur_b, expression_a + expression_b + ["*"]),
                ]
                if valeur_a > valeur_b:
                    operations.append((valeur_a - valeur_b, expression_a + expression_b + ["-"]))
                if valeur_b > valeur_a:
                    operations.append((valeur_b - valeur_a, expression_b + expression_a + ["-"]))
                if valeur_b != 0 and valeur_a % valeur_b == 0:
                    operations.append((valeur_a // valeur_b, expression_a + expression_b + ["/"]))
                if valeur_a != 0 and valeur_b % valeur_a == 0:
                    operations.append((valeur_b // valeur_a, expression_b + expression_a + ["/"]))

                nb_noeuds += 6
                for nouvelle_valeur, nouvelle_expression in operations:
                    if nouvelle_valeur == cible:
                        meilleure_expression = nouvelle_expression
                        print(" ".join(map(str, nouvelle_expression)), "=", nouvelle_valeur)
                        return True

                    distance = abs(cible - nouvelle_valeur)
                    if distance < meilleure_distance:
                        meilleure_distance = distance
                        meilleure_expression = nouvelle_expression
                        print(" ".join(map(str, nouvelle_expression)), "=", nouvelle_valeur)

                    nouvel_etat = restants + [(nouvelle_valeur, nouvelle_expression)]
                    signature = tuple(sorted(valeur for valeur, _ in nouvel_etat))
                    if signature not in etats_vus:
                        etats_vus.add(signature)
                        if parcours_DFSR_aux(nouvel_etat):
                            return True

        return False

    etat_initial = [(carton, [carton]) for carton in cartons]
    parcours_DFSR_aux(etat_initial)

    return meilleure_expression, nb_noeuds


if __name__ == "__main__":
    parcours_DFS([3,5, 7, 9, 25, 50], 859)
    parcours_BFS([3,5, 7, 9, 25, 50], 859)
    parcours_DFS_recursif([3,5, 7, 9, 25, 50], 859)
 

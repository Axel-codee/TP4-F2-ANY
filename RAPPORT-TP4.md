# TP4 — Le compte est bon : comparaison des parcours

## Méthode

J'ai comparé trois façons de parcourir l'arbre des calculs : DFS avec une pile, DFS
récursif et BFS avec une file. À chaque étape, on prend deux valeurs disponibles et on
les remplace par le résultat d'une opération. L'expression est gardée en notation
polonaise inverse (NPI) pour pouvoir afficher la solution. On peut atteindre la cible
sans utiliser tous les cartons.

Pour chaque paire, le programme essaie l'addition, la multiplication, les deux sens de
la soustraction et les deux sens de la division. Il écarte les résultats nuls ou négatifs
et les divisions non entières. Il évite aussi de revisiter un état si le même ensemble
de valeurs a déjà été obtenu autrement. Cela ne change pas les calculs possibles à
partir de cet état, mais évite d'explorer plusieurs fois la même suite.

Les parcours s'arrêtent dès qu'ils trouvent la cible. Sinon, ils renvoient l'expression
qui donne la valeur la plus proche.

## Mesures

J'ai compté comme **nœud** la situation initiale puis chaque opération tentée, y
compris celles qui sont invalides ou qui mènent à un état déjà vu. La **hauteur** est
le nombre maximal d'opérations dans une branche générée ; la **largeur** est le plus
grand nombre d'états distincts générés à une même profondeur. La dernière mesure de
mémoire est la taille maximale de la pile ou de la file. Pour le DFS récursif, c'est
le nombre maximal d'appels imbriqués. Le DFS avec pile ne stocke qu'un cadre par
niveau : il ne met pas tous les calculs frères dans la pile.

Les temps ci-dessous sont les médianes de cinq essais par parcours, en millisecondes.
Ils comprennent la recherche et ses affichages (redirigés en mémoire), mais pas le
lancement de Python. La commande `python experimentation_tp4.py 5` permet de refaire
les mesures. J'ai pris la graine `17081936` donnée en exemple dans l'énoncé ; pour les
cas impossible et ardu, j'ai fixé le premier tirage de chaque liste du générateur afin
de comparer les parcours sur exactement les mêmes problèmes.

## Résultats

| Tirage → cible | Parcours | Nœuds | Pile/file max | Hauteur | Largeur | Meilleur résultat | Temps médian (ms) |
|---|---|---:|---:|---:|---:|---:|---:|
| 4 5 10 75 7 4 → 319 | DFS | 3 136 | 6 | 5 | 544 | 319 | 4,213 |
| 4 5 10 75 7 4 → 319 | DFS récursif | 3 136 | 6 | 5 | 544 | 319 | 3,447 |
| 4 5 10 75 7 4 → 319 | BFS | 23 264 | 4 239 | 4 | 3 596 | 319 | 28,689 |
| 7 7 8 9 9 25 → 365 (impossible) | DFS | 75 595 | 6 | 5 | 5 174 | 366 | 87,956 |
| 7 7 8 9 9 25 → 365 (impossible) | DFS récursif | 75 595 | 6 | 5 | 5 174 | 366 | 73,851 |
| 7 7 8 9 9 25 → 365 (impossible) | BFS | 75 595 | 5 452 | 5 | 5 174 | 366 | 82,482 |
| 1 4 6 25 50 100 → 263 (ardu) | DFS | 36 129 | 6 | 5 | 3 143 | 263 | 44,442 |
| 1 4 6 25 50 100 → 263 (ardu) | DFS récursif | 36 129 | 6 | 5 | 3 143 | 263 | 37,142 |
| 1 4 6 25 50 100 → 263 (ardu) | BFS | 137 203 | 14 593 | 5 | 14 314 | 263 | 165,823 |

## Ce que j'en retiens

Sur ces trois tirages, le DFS récursif a été le plus rapide. Le DFS avec pile visite les
mêmes calculs dans le même ordre, mais coûte un peu plus de temps. Sur le premier
tirage, le BFS trouve 319 en quatre opérations au lieu de cinq avec DFS ; en revanche,
il examine plus de sept fois plus de nœuds et sa file monte à 4 239 états.

Le cas impossible oblige à terminer toute la recherche : les trois parcours examinent
alors 75 595 tentatives et donnent 366, à une unité de la cible. Parmi ces tentatives,
35 044 étaient invalides et 29 204 conduisaient à un état déjà vu. Le BFS garde bien
plus d'états en mémoire que les deux DFS, même quand il ne parcourt pas davantage de
nœuds. Le meilleur choix dépend donc de ce que l'on cherche : une solution avec peu
d'opérations, ou une recherche peu coûteuse en mémoire et en temps sur ces exemples.

Les tests (`python -m unittest discover -v`) vérifient notamment les expressions NPI,
l'arrêt à la cible et les comptages. Les chiffres de temps peuvent varier d'une machine
à l'autre.

# power_bdd

Creates the ROBDD of a weighted game and calculates power indices according to Banzhaf/Penrose and Shapley/Shubik.
This method allows to easily connect bdds with AND or OR and is also suited for voting systems with multiple layers.
The method was published by S. Bolus:
* [Bolus, S., 2011. Power indices of simple games and vector-weighted majority games by means of binary decision diagrams. European J. Oper. Res. 210 (2), 258–272.](https://www.sciencedirect.com/science/article/abs/pii/S0377221710006181)
* If you are interested in calculating power indices you should also check out the [website](https://www.informatik.uni-kiel.de/~progsys/simple_games/lab/lab.html), which offers a javascript-version with a lot more features.

# Usage

## Installation
    pip install power_bdd

## Import
    from power_bdd.bdd import BDD, WeightedGame

## one-tier games
This example calculates the power indices for the electoral college, 1996.

    w = [54, 33, 32, 25, 23, 22, 21, 18, 15, 14, 13, 13, 12, 12, 11, 11, 11, 11, 10, 10, 9, 9, 8, 8, 8, 8, 8, 8, 7, 7, 7, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3]                
    q = 270
    game = WeightedGame(q, w)
    bdd = BDD(game)
    banzhaf = bdd.calc_banzhaf()
    shapley = bdd.calc_shapley()
    print(banzhaf)
    print(shapley)

## multi-tier games
This example calculates the power-indices for the U.S. federal system, which can represented by the weighted voting systems
_G = (G1 and G2 and G3) or (G1 and G4 and G5 and G3) or (G6 and G7)_, 
see https://www.fernuni-hagen.de/stochastik/downloads/voting.pdf.

    game1 = WeightedGame(218, [0, 0] + [0] * 100 + [1] * 435)
    game2 = WeightedGame(51,  [0, 0] + [1] * 100 + [0] * 435)
    game3 = WeightedGame(1,   [1, 0] + [0] * 100 + [0] * 435)
    game4 = WeightedGame(50,  [0, 0] + [1] * 100 + [0] * 435)
    game5 = WeightedGame(1,   [0, 1] + [0] * 100 + [0] * 435)
    game6 = WeightedGame(290, [0, 0] + [0] * 100 + [1] * 435)
    game7 = WeightedGame(67,  [0, 0] + [1] * 100 + [0] * 435)

    federal_system = BDD(game1) & BDD(game2) & BDD(game3) | BDD(game1) & BDD(game4) & BDD(game5) & BDD(game3) | BDD(game6) & BDD(game7)
    banzhaf = federal_system.calc_banzhaf()
    print(banzhaf)

# Complexities
Listed complexities are expected complexities for the computation of all voters. At first glance, the complexities seem partly worse than other methods (e.g. using _dynamic programming_), but there are several hidden benefitial properties, for instance _q_ is not necessary the _q_ input _q_, but the smallest integer that is possible to use as quota to represent the game (with any weights).

## one-tier games:

    power-index     | time          | space       
    ------------    | ------------- | ------------
    Banzhaf/Penrose | O(nq log(q))  | O(nq)
    Shapley/Shubik  | O(n^3q)       | O(n^2q)

## multi-tier games with _m_ tiers:

    power-index     | time                   | space       
    ------------    | -------------          | ------------
    Banzhaf/Penrose | O(n prod_{t=1}^m q^t)  | O(n prod_{t=1}^m q^t)
    Shapley/Shubik  | O(n^3 prod_{t=1}^m q^t)| O(n^2 prod_{t=1}^m q^t)

# Remarks
* My java-version is much faster (somewhere between 10-100 times) so there should be plenty of room for optimization in python.
* The original version uses an AVL-tree for the _create_-method. I have replaced that by a _SortedList_ form the _sortedcontainers_-library.    
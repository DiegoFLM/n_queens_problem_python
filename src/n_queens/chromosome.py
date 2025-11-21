"""
Chromosome module for N-Queens problem.

This module contains the Chromosome class which represents a single solution
candidate for the N-Queens problem using a permutation-based encoding.
"""

import math
from typing import Optional

import numpy as np
import numpy.typing as npt


class Chromosome:
    """
    Represents a chromosome (solution candidate) for the N-Queens problem.

    The chromosome uses permutation encoding where the index represents the column
    and the value represents the row position of the queen in that column.
    This encoding guarantees no two queens are in the same row or column.

    Attributes:
        __n: The size of the chessboard (N x N).
        __positions: NumPy array representing queen positions.

    Example:
        >>> chromosome = Chromosome(np.array([1, 3, 0, 2]))
        >>> chromosome.get_n()
        4
        >>> chromosome.get_positions()
        array([1, 3, 0, 2])
    """

    def __init__(self, arr: npt.ArrayLike) -> None:
        """
        Initialize a chromosome with given queen positions.

        Args:
            arr: Array-like object containing queen positions for each column.
                 Length determines the board size N.
        """
        self.__n: int = len(arr)
        self.__positions: npt.NDArray[np.int_] = np.array(arr)

    def get_n(self) -> int:
        """
        Get the size of the chessboard.

        Returns:
            The dimension N of the N x N chessboard.
        """
        return self.__n

    def get_positions(self) -> npt.NDArray[np.int_]:
        """
        Get the queen positions for this chromosome.

        Returns:
            NumPy array where index is column and value is row position.
        """
        return self.__positions

    def print_board(self) -> None:
        """
        Print a visual representation of the chessboard.

        Queens are represented by 15, empty squares by 0.
        """
        board = np.zeros((len(self.__positions), len(self.__positions)), dtype=int)
        for i, pos in enumerate(self.__positions):
            board[pos][i] = 15
        print(board)

    def random_vec(self) -> npt.NDArray[np.int_]:
        """
        Generate a random valid chromosome configuration.

        Creates a random permutation with a constraint: the first column's queen
        must be in the upper half of the board to reduce symmetrical duplicates.

        Returns:
            NumPy array representing a random valid queen configuration.
        """
        pool = np.arange(self.__n)
        chr = np.zeros(self.__n, dtype=int)

        # First queen constrained to upper half
        r = np.random.randint(0, 1 + math.floor((self.__n - 1) / 2))
        chr[0] = r
        pool = np.delete(pool, r)

        # Remaining queens randomly placed
        for i in range(1, self.__n):
            r = np.random.randint(0, len(pool))
            chr[i] = pool[r]
            pool = np.delete(pool, r)

        return chr

    def make_child(self) -> "Chromosome":
        """
        Create a mutated child chromosome by swapping two positions.

        Implements swap mutation: randomly selects two columns and swaps
        their queen positions. Includes special handling to maintain the
        first-column constraint.

        Returns:
            A new Chromosome instance with swapped positions.
        """
        if self.__n <= 2:
            return Chromosome(self.__positions.copy())

        mutant = self.__positions.copy()
        cols_pool = np.arange(self.__n)
        c1, c2 = np.random.choice(cols_pool, size=2, replace=False)
        cols_pool = np.delete(cols_pool, np.where(cols_pool == c1))

        # Ensure first column constraint is maintained
        if c1 == 0 and self.__positions[c2] > math.floor((self.__n - 1) / 2):
            while self.__positions[c2] > math.floor((self.__n - 1) / 2):
                cols_pool = np.delete(cols_pool, np.where(cols_pool == c2))
                c2 = np.random.choice(cols_pool)
        elif (c2 == 0 and
              self.__positions[c1] > math.floor((self.__n - 1) / 2)):
            cols_pool = np.delete(cols_pool, 0)
            c2 = np.random.choice(cols_pool)

        c1, c2 = min(c1, c2), max(c1, c2)
        mutant[c1], mutant[c2] = mutant[c2], mutant[c1]
        return Chromosome(mutant)

    def mutual_threats(self) -> int:
        """
        Calculate the number of mutual diagonal threats between queens.

        A mutual threat occurs when two queens are on the same diagonal.
        The permutation encoding guarantees no row or column conflicts.
        All queen pairs are checked, even if other queens are between them.

        Returns:
            Number of queen pairs attacking each other diagonally.

        Note:
            Maximum threats = N*(N-1)/2 when all queens on same diagonal.
            Minimum threats = 0 for a valid solution.
        """
        threats = 0
        for i in range(self.__n):
            for j in range(i + 1, self.__n):
                # Queens on same diagonal if column distance == row distance
                if abs(i - j) == abs(self.__positions[i] - self.__positions[j]):
                    threats += 1
        return threats

    def fitness(self) -> float:
        """
        Calculate the normalized fitness of this chromosome.

        Fitness is normalized to [0, 1] where 1 represents a perfect solution
        (no conflicts) and 0 represents maximum conflicts.

        Returns:
            Float between 0 and 1 representing solution quality.

        Note:
            Prints "SOLUTION FOUND" message when fitness equals 1.0.
        """
        max_threats = self.__n * (self.__n - 1) / 2
        if self.__n <= 1:
            return 1.0

        fitness = (max_threats - self.mutual_threats()) / max_threats
        if fitness == 1:
            print(f"SOLUTION FOUND: {self.get_positions()}", end=" ")
        return fitness

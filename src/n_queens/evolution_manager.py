"""
Evolution Manager module for N-Queens problem.

This module contains the EvolManager class which implements multiple algorithmic
approaches to solve the N-Queens problem: genetic algorithm, Las Vegas, and Monte Carlo.
"""

import math
import random
import time
from typing import List, Optional

import numpy as np
import numpy.typing as npt

from .chromosome import Chromosome


class EvolManager:
    """
    Manages evolutionary algorithms for solving the N-Queens problem.

    This class implements three different approaches:
    1. Greedy Evolution (Genetic Algorithm)
    2. Las Vegas Algorithm (randomized, guaranteed correct)
    3. Monte Carlo Algorithm (probabilistic estimation)

    Attributes:
        __n: Size of the chessboard (N x N).
        __population: Number of chromosomes in the population.
        __generations: Maximum number of generations to evolve.
        __current_generation: Current generation number.
        __chrom_array: List of chromosomes in current population.
        __solutions: List of unique solutions found.
        __sol_generations: Generations when each solution was found.
        __reproductive_pool: Chromosomes selected for breeding.
        __sorted_chrom_array: Population sorted by fitness.
        __reproductive_pool_size: Size of the reproductive pool.
        __offspring: List of offspring chromosomes.
        __offspring_size: Number of offspring to generate.
        __big_array: Combined population and offspring for selection.
        __solution_times: Time taken to find each solution.
        __mutation_rate: Mutation rate (currently unused).
        __reproductive_coefficient: Selection probability multiplier.
        __starting_time: Timestamp when algorithm started.
    """

    def __init__(
        self,
        genes_per_chrom: int,
        pop: int,
        generations: int,
        reproductive_pool_size: Optional[int] = None,
        offspring: Optional[int] = None,
        mutation_rate: float = 0.2,
        reproductive_coefficient: float = 1 / 3,
    ) -> None:
        """
        Initialize the Evolution Manager.

        Args:
            genes_per_chrom: Size of the chessboard (N).
            pop: Population size.
            generations: Maximum number of generations.
            reproductive_pool_size: Number of chromosomes for breeding.
                                   Defaults to 80% of population.
            offspring: Number of children per generation.
                      Defaults to 1.5x reproductive pool size.
            mutation_rate: Mutation rate (reserved for future use).
            reproductive_coefficient: Probability multiplier for selection.
        """
        if reproductive_pool_size is None:
            reproductive_pool_size = math.floor(pop * 0.8)

        if offspring is None:
            offspring = math.floor(reproductive_pool_size * 1.5)

        self.__n: int = genes_per_chrom
        self.__population: int = pop
        self.__generations: int = generations
        self.__current_generation: int = 0
        self.__chrom_array: List[Chromosome] = []
        self.__solutions: List[Chromosome] = []
        self.__sol_generations: npt.NDArray[np.int_] = np.array([], dtype=int)
        self.__reproductive_pool: List[Chromosome] = []
        self.__sorted_chrom_array: List[Chromosome] = []
        self.__reproductive_pool_size: int = reproductive_pool_size
        self.__offspring: List[Chromosome] = []
        self.__offspring_size: int = int(offspring)
        self.__big_array: List[Chromosome] = []
        self.__solution_times: npt.NDArray[np.float64] = np.array([], dtype=float)
        self.__mutation_rate: float = mutation_rate
        self.__reproductive_coefficient: float = reproductive_coefficient
        self.__starting_time: Optional[float] = None

        self.populate()

    def populate(self) -> None:
        """
        Initialize the population with random chromosomes.

        Creates the initial population and identifies any perfect solutions.
        Solutions found during initialization are tracked separately.
        """
        proto_chrom = Chromosome(list(range(self.__n)))

        for i in range(self.__population):
            self.__chrom_array.append(Chromosome(proto_chrom.random_vec()))

        # Check for solutions in initial population
        for i in range(len(self.__chrom_array)):
            new_sol = True
            if self.__chrom_array[i].fitness() == 1.00:
                for j in range(len(self.__solutions)):
                    if np.array_equal(
                        self.__chrom_array[i].get_positions(),
                        self.__solutions[j].get_positions()
                    ):
                        new_sol = False
                        break
                if new_sol:
                    self.__solutions.append(self.__chrom_array[i])
                    self.__sol_generations = np.append(
                        self.__sol_generations, self.__current_generation
                    )
                    self.__solution_times = np.append(self.__solution_times, 0.0)
        print("It's populated over here!")

    def get_chrom_array(self) -> List[Chromosome]:
        """Get the current population."""
        return self.__chrom_array

    def get_solutions(self) -> List[Chromosome]:
        """Get all unique solutions found."""
        return self.__solutions

    def get_solution_times(self) -> npt.NDArray[np.float64]:
        """Get time taken to find each solution."""
        return self.__solution_times

    def get_sol_generations(self) -> npt.NDArray[np.int_]:
        """Get generation number when each solution was found."""
        return self.__sol_generations

    def get_best_chrom_fitness(self) -> float:
        """
        Get the fitness of the best chromosome in current population.

        Returns:
            Fitness value of the fittest chromosome.
        """
        ordered_popul = sorted(
            self.__chrom_array, key=lambda chrom: -chrom.fitness()
        )
        return ordered_popul[0].fitness()

    def get_best_chrom_mutual_threats(self) -> int:
        """
        Get the number of threats for the best chromosome.

        Returns:
            Number of mutual threats for the fittest chromosome.
        """
        ordered_popul = sorted(
            self.__chrom_array, key=lambda chrom: -chrom.fitness()
        )
        return ordered_popul[0].mutual_threats()

    def get_reproductive_pool(self) -> List[Chromosome]:
        """Get the current reproductive pool."""
        return self.__reproductive_pool

    def get_offspring(self) -> List[Chromosome]:
        """Get the current offspring."""
        return self.__offspring

    def get_current_generation(self) -> int:
        """Get the current generation number."""
        return self.__current_generation

    def set_chrom_array(self, vec_array: List[npt.ArrayLike]) -> None:
        """
        Replace the current population with new chromosomes.

        Args:
            vec_array: List of arrays representing chromosome positions.
        """
        self.__n = len(vec_array[0])
        self.__population = len(vec_array)
        self.__current_generation = 0
        self.__chrom_array = []
        self.__solutions = []
        self.__sol_generations = np.array([], dtype=int)
        self.__reproductive_pool = []
        self.__sorted_chrom_array.clear()
        self.__offspring.clear()
        self.__big_array.clear()
        self.__solution_times = np.array([], dtype=float)

        for i in vec_array:
            self.__chrom_array.append(Chromosome(i))

    def show_chromosomes_positions(self) -> None:
        """Print positions and fitness of all chromosomes in population."""
        print("__chrom_array members: ")
        for i in self.__chrom_array:
            print(f"{i.get_positions()}", end=" ")
            print(f"fitness: {i.fitness()}")

    def show_solutions(self) -> None:
        """
        Print all solutions found with their metadata.

        Displays solution positions, generation found, and time taken.
        """
        print("Solutions: ")
        for i in range(len(self.__solutions)):
            print(
                f"solution [{i}]: {self.__solutions[i].get_positions()}.",
                end=" "
            )
            if len(self.__sol_generations) > 0:
                print(f"Generation: {self.__sol_generations[i]}", end=" ")
            print(f"Time: {self.__solution_times[i]}")

        if len(self.__solutions) > 2:
            if (self.__solutions[len(self.__solutions) - 1].get_positions()
                    == self.__solutions[len(self.__solutions) - 2].get_positions()).all():
                print("last solution repeated")

    def make_reproductive_pool(self) -> None:
        """
        Select chromosomes for breeding based on fitness.

        Implements fitness-proportional selection with special handling
        for perfect solutions (removes them from population to find
        diverse solutions).
        """
        self.__reproductive_pool.clear()

        # Sort chromosomes by fitness in descending order
        self.__sorted_chrom_array = sorted(
            self.__chrom_array, key=lambda crom: -crom.fitness()
        )

        c = 0
        while len(self.__reproductive_pool) < self.__reproductive_pool_size:
            bool_signal = False
            d = c % len(self.__sorted_chrom_array)

            if len(self.__sorted_chrom_array) <= (self.__population / 2):
                self.__sorted_chrom_array.append(
                    Chromosome(self.__chrom_array[0].random_vec())
                )

            elif self.__n <= 2 or (
                c > self.__population and len(self.__reproductive_pool) == 0
            ):
                self.__reproductive_pool = self.__sorted_chrom_array[
                    :self.__reproductive_pool_size
                ]

            # Fitness-proportional selection
            elif random.random() < (
                self.__sorted_chrom_array[d].fitness()
                * self.__reproductive_coefficient
            ):
                self.__reproductive_pool.append(self.__sorted_chrom_array[d])

            # Handle perfect solutions
            if self.__sorted_chrom_array[d].fitness() == 1.000000:
                if len(self.__solutions) == 0:
                    self.__solutions.append(self.__sorted_chrom_array[d])
                    self.__sol_generations = np.append(
                        self.__sol_generations, self.__current_generation
                    )
                    ending = time.perf_counter()
                    lapse = ending - self.__starting_time
                    self.__solution_times = np.append(self.__solution_times, lapse)
                    print("Time for first solution:")
                    print(lapse)

                    self.__chrom_array.append(
                        Chromosome(self.__chrom_array[0].random_vec())
                    )
                    self.__chrom_array.remove(self.__sorted_chrom_array[d])
                    self.__sorted_chrom_array.pop(d)
                    continue

                # Check if solution is unique
                for i in range(len(self.__solutions)):
                    if (self.__solutions[i].get_positions()
                            == self.__sorted_chrom_array[d].get_positions()).all():
                        self.__chrom_array.append(
                            Chromosome(self.__chrom_array[0].random_vec())
                        )
                        if self.__sorted_chrom_array[d] in self.__chrom_array:
                            self.__chrom_array.remove(self.__sorted_chrom_array[d])

                        if self.__sorted_chrom_array[d] in self.__reproductive_pool:
                            self.__reproductive_pool.remove(
                                self.__sorted_chrom_array[d]
                            )

                        self.__sorted_chrom_array.pop(d)
                        bool_signal = True
                        break

                if bool_signal:
                    continue
                else:
                    self.__solutions.append(self.__sorted_chrom_array[d])
                    self.__sol_generations = np.append(
                        self.__sol_generations, self.__current_generation
                    )
                    ending = time.perf_counter()
                    lapse = ending - self.__starting_time
                    self.__solution_times = np.append(self.__solution_times, lapse)
                    print(f"Time for new solution: {lapse}")

            c += 1

    def reproductive_season(self) -> None:
        """
        Generate offspring from the reproductive pool.

        Each offspring is created by mutating a parent from the
        reproductive pool using round-robin selection.
        """
        self.__offspring.clear()
        for i in range(self.__offspring_size):
            self.__offspring.append(
                self.__reproductive_pool[i % len(self.__reproductive_pool)].make_child()
            )

    def replacement(self) -> None:
        """
        Select survivors for the next generation.

        Combines parents and offspring, then selects the fittest
        individuals to form the next generation (elitism).
        """
        self.__big_array = self.__chrom_array + self.__offspring
        self.__big_array = sorted(self.__big_array, key=lambda crom: -crom.fitness())
        self.__chrom_array = self.__big_array[:self.__population]

    def greedy_next_generation(self) -> None:
        """
        Execute one generation of the genetic algorithm.

        Performs selection, reproduction, and replacement.
        """
        print(f"Current generation: {self.__current_generation}")
        self.make_reproductive_pool()
        self.reproductive_season()
        self.replacement()

    def greedy_evolution(self) -> None:
        """
        Run the complete genetic algorithm.

        Evolves the population for the specified number of generations
        and reports results.
        """
        self.__current_generation = 0
        self.__chrom_array.clear()
        self.__solutions.clear()
        self.__sol_generations = np.array([], dtype=int)
        self.__reproductive_pool.clear()
        self.__sorted_chrom_array.clear()
        self.__offspring.clear()
        self.__big_array.clear()
        self.__solution_times = np.array([], dtype=float)

        self.populate()
        self.__starting_time = time.perf_counter()

        while self.__current_generation < self.__generations:
            self.greedy_next_generation()
            self.__current_generation += 1

        print(f"Current generation: {self.__current_generation}")
        print(f"Population: {self.__population}")
        self.show_chromosomes_positions()
        self.show_solutions()

    def las_vegas(self, attempts: int) -> None:
        """
        Run Las Vegas algorithm to find solutions.

        Repeatedly generates random chromosomes until solutions are found.
        Guarantees correctness but runtime is unpredictable.

        Args:
            attempts: Maximum number of random chromosomes to try.
        """
        self.__current_generation = 0
        self.__chrom_array.clear()
        self.__solutions.clear()
        self.__sol_generations = np.array([], dtype=int)
        self.__reproductive_pool.clear()
        self.__sorted_chrom_array.clear()
        self.__offspring.clear()
        self.__big_array.clear()
        self.__solution_times = np.array([], dtype=float)
        self.__starting_time = time.perf_counter()

        proto_chrom = Chromosome(list(range(self.__n)))

        for a in range(attempts):
            chro = Chromosome(proto_chrom.random_vec())

            if chro.fitness() == 1.000000:
                new_sol = True
                for j in range(len(self.__solutions)):
                    if np.array_equal(
                        chro.get_positions(),
                        self.__solutions[j].get_positions()
                    ):
                        new_sol = False
                        break
                if new_sol:
                    self.__solutions.append(chro)
                    self.__solution_times = np.append(
                        self.__solution_times,
                        time.perf_counter() - self.__starting_time
                    )

    def montecarlo(self, attempts: int) -> float:
        """
        Run Monte Carlo algorithm to estimate solution probability.

        Generates random chromosomes and calculates the proportion
        that are valid solutions.

        Args:
            attempts: Number of random samples to generate.

        Returns:
            Ratio of solutions found to total attempts.
        """
        self.__current_generation = 0
        self.__chrom_array.clear()
        self.__solutions.clear()
        self.__sol_generations = np.array([], dtype=int)
        self.__reproductive_pool.clear()
        self.__sorted_chrom_array.clear()
        self.__offspring.clear()
        self.__big_array.clear()
        self.__solution_times = np.array([], dtype=float)
        self.__starting_time = time.perf_counter()

        proto_chrom = Chromosome(list(range(self.__n)))
        found_solutions = 0

        for a in range(attempts):
            chro = Chromosome(proto_chrom.random_vec())

            if chro.fitness() == 1.000000:
                found_solutions += 1
                self.__solution_times = np.append(
                    self.__solution_times,
                    time.perf_counter() - self.__starting_time
                )

        return found_solutions / attempts

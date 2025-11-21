"""
N-Queens Problem Solver Package.

This package provides multiple algorithmic approaches to solve the N-Queens problem:
- Genetic Algorithm (Greedy Evolution)
- Las Vegas Algorithm
- Monte Carlo Algorithm

Example:
    >>> from n_queens import Chromosome, EvolManager
    >>> manager = EvolManager(genes_per_chrom=8, pop=100, generations=50)
    >>> manager.greedy_evolution()
"""

from .chromosome import Chromosome
from .evolution_manager import EvolManager
from . import visualization

__version__ = "1.0.0"
__all__ = ["Chromosome", "EvolManager", "visualization"]

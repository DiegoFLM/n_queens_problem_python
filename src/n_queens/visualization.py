"""
Visualization utilities for N-Queens problem solutions.

This module provides functions to visualize chess boards, performance metrics,
and algorithm comparisons.
"""

from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import numpy.typing as npt
from matplotlib.figure import Figure

from .chromosome import Chromosome


def render_board(
    positions: npt.NDArray[np.int_],
    title: str = "N-Queens Solution",
    figsize: Tuple[int, int] = (8, 8),
    save_path: Optional[str] = None
) -> Figure:
    """
    Render a chessboard with queens placed according to positions array.

    Args:
        positions: Array where index is column and value is row position.
        title: Title for the plot.
        figsize: Figure size as (width, height).
        save_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    n = len(positions)
    fig, ax = plt.subplots(figsize=figsize)

    # Draw chessboard squares
    for row in range(n):
        for col in range(n):
            color = '#F0D9B5' if (row + col) % 2 == 0 else '#B58863'
            square = patches.Rectangle(
                (col, n - 1 - row), 1, 1,
                linewidth=1,
                edgecolor='black',
                facecolor=color
            )
            ax.add_patch(square)

    # Place queens
    for col, row in enumerate(positions):
        ax.text(
            col + 0.5,
            n - 1 - row + 0.5,
            '♛',
            fontsize=min(400 / n, 60),
            ha='center',
            va='center',
            color='#000000',
            weight='bold'
        )

    # Set up axes
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=16, weight='bold', pad=20)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def render_multiple_solutions(
    solutions: List[Chromosome],
    max_display: int = 6,
    save_path: Optional[str] = None
) -> Figure:
    """
    Render multiple solutions in a grid layout.

    Args:
        solutions: List of Chromosome objects representing solutions.
        max_display: Maximum number of solutions to display.
        save_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    num_solutions = min(len(solutions), max_display)
    n = solutions[0].get_n()

    cols = min(3, num_solutions)
    rows = (num_solutions + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))

    if num_solutions == 1:
        axes = np.array([axes])
    axes = axes.flatten() if num_solutions > 1 else axes

    for idx, solution in enumerate(solutions[:max_display]):
        ax = axes[idx] if num_solutions > 1 else axes[0]
        positions = solution.get_positions()

        # Draw chessboard
        for row in range(n):
            for col in range(n):
                color = '#F0D9B5' if (row + col) % 2 == 0 else '#B58863'
                square = patches.Rectangle(
                    (col, n - 1 - row), 1, 1,
                    linewidth=0.5,
                    edgecolor='black',
                    facecolor=color
                )
                ax.add_patch(square)

        # Place queens
        for col, row in enumerate(positions):
            ax.text(
                col + 0.5,
                n - 1 - row + 0.5,
                '♛',
                fontsize=min(300 / n, 40),
                ha='center',
                va='center',
                color='#000000',
                weight='bold'
            )

        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Solution {idx + 1}', fontsize=12, weight='bold')

    # Hide unused subplots
    for idx in range(num_solutions, len(axes)):
        axes[idx].axis('off')

    plt.suptitle(f'{n}-Queens Problem: Multiple Solutions',
                 fontsize=16, weight='bold', y=0.98)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def plot_fitness_evolution(
    fitness_history: List[float],
    title: str = "Fitness Evolution Over Generations",
    save_path: Optional[str] = None
) -> Figure:
    """
    Plot fitness values over generations.

    Args:
        fitness_history: List of fitness values per generation.
        title: Plot title.
        save_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    generations = range(len(fitness_history))
    ax.plot(generations, fitness_history, linewidth=2, color='#2E86AB')
    ax.fill_between(generations, fitness_history, alpha=0.3, color='#2E86AB')

    ax.set_xlabel('Generation', fontsize=12, weight='bold')
    ax.set_ylabel('Best Fitness', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim(0, 1.05)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def plot_performance_comparison(
    algorithms: List[str],
    times: List[float],
    solutions_found: List[int],
    save_path: Optional[str] = None
) -> Figure:
    """
    Create bar charts comparing algorithm performance.

    Args:
        algorithms: List of algorithm names.
        times: Time taken by each algorithm (seconds).
        solutions_found: Number of solutions found by each algorithm.
        save_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = ['#2E86AB', '#A23B72', '#F18F01']
    x_pos = np.arange(len(algorithms))

    # Time comparison
    bars1 = ax1.bar(x_pos, times, color=colors[:len(algorithms)], alpha=0.8)
    ax1.set_xlabel('Algorithm', fontsize=12, weight='bold')
    ax1.set_ylabel('Time (seconds)', fontsize=12, weight='bold')
    ax1.set_title('Time to Find Solutions', fontsize=14, weight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(algorithms, rotation=15, ha='right')
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}s',
                ha='center', va='bottom', fontsize=10)

    # Solutions comparison
    bars2 = ax2.bar(x_pos, solutions_found, color=colors[:len(algorithms)], alpha=0.8)
    ax2.set_xlabel('Algorithm', fontsize=12, weight='bold')
    ax2.set_ylabel('Number of Solutions', fontsize=12, weight='bold')
    ax2.set_title('Solutions Found', fontsize=14, weight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(algorithms, rotation=15, ha='right')
    ax2.grid(True, alpha=0.3, axis='y', linestyle='--')

    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10)

    plt.suptitle('Algorithm Performance Comparison',
                 fontsize=16, weight='bold', y=1.02)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig


def plot_solution_distribution(
    solution_times: npt.NDArray[np.float64],
    title: str = "Solution Discovery Timeline",
    save_path: Optional[str] = None
) -> Figure:
    """
    Plot when solutions were discovered over time.

    Args:
        solution_times: Array of timestamps when solutions were found.
        title: Plot title.
        save_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    solution_numbers = range(1, len(solution_times) + 1)
    ax.scatter(solution_times, solution_numbers, s=100,
              color='#2E86AB', alpha=0.6, edgecolors='black', linewidth=1.5)
    ax.plot(solution_times, solution_numbers, color='#2E86AB',
           alpha=0.3, linestyle='--', linewidth=2)

    ax.set_xlabel('Time (seconds)', fontsize=12, weight='bold')
    ax.set_ylabel('Solution Number', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')

    return fig

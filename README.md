# N-Queens Problem Solver

<p align="center">
  <strong>A professional Python implementation of genetic algorithms, Las Vegas, and Monte Carlo methods for solving the N-Queens problem</strong>
</p>

<p align="center">
  <img src="docs/images/8queens_solution.png" alt="8-Queens Solution" width="400"/>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#algorithms">Algorithms</a> •
  <a href="#visualizations">Visualizations</a> •
  <a href="#documentation">Documentation</a>
</p>

---

## Table of Contents

- [Quick Start](#quick-start)
- [Problem Description](#problem-description)
- [Features](#features)
- [Visualizations](#visualizations)
- [Installation](#installation)
- [Usage](#usage)
  - [Genetic Algorithm](#running-the-genetic-algorithm)
  - [Las Vegas Algorithm](#running-las-vegas-algorithm)
  - [Monte Carlo Algorithm](#running-monte-carlo-algorithm)
  - [Visualizations](#using-visualizations)
- [Algorithms](#algorithms)
- [Project Structure](#project-structure)
- [Results & Performance](#results--performance)
- [Examples & Notebooks](#examples--notebooks)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

---

## Quick Start

Get started in under 2 minutes:

```bash
# Clone and navigate
git clone <repository-url>
cd n_queens_problem_python

# Install dependencies
pip install -r requirements.txt

# Run a quick 8-Queens example
python -c "
from n_queens import EvolManager
manager = EvolManager(genes_per_chrom=8, pop=100, generations=30)
manager.greedy_evolution()
"
```

**Want to explore?** Check out the [interactive notebooks](notebooks/) for detailed demonstrations and analysis.

---

## Problem Description

The **N-Queens problem** is a classic combinatorial puzzle where the goal is to place N chess queens on an N×N chessboard such that no two queens threaten each other.

**Constraints:**
- ✓ No two queens share the same **row**
- ✓ No two queens share the same **column**
- ✓ No two queens share the same **diagonal**

**Example:** For N=8, there are **92 distinct solutions**. This project uses intelligent algorithms to find them efficiently.

---

## Features

### 🧬 **Multiple Algorithmic Approaches**
- **Genetic Algorithm** - Evolutionary computation with fitness-based selection
- **Las Vegas Algorithm** - Randomized approach guaranteeing correct solutions
- **Monte Carlo Algorithm** - Probabilistic estimation of solution density

### 🎯 **Optimized Implementation**
- **Permutation encoding** - Guarantees no row/column conflicts
- **Normalized fitness function** - Efficient solution quality evaluation
- **Type-safe code** - Full type hints using Python's typing module
- **Comprehensive docstrings** - Google-style documentation throughout

### 📊 **Professional Visualizations**
- Chess board rendering with queen symbols ♛
- Multi-solution grid displays
- Fitness evolution plots
- Algorithm performance comparisons
- Solution discovery timelines

### 🔧 **Developer-Friendly**
- Well-organized package structure
- Interactive Jupyter notebooks
- Configurable algorithm parameters
- Performance tracking and statistics
- Easy-to-extend architecture

### 📚 **Educational Resources**
- Three detailed demonstration notebooks
- Statistical analysis examples
- Algorithm comparison benchmarks
- Comprehensive README and docs

---

## Visualizations

The project includes professional visualization capabilities for analysis and presentation.

<details>
<summary><b>Click to view visualization examples</b></summary>

### Multiple Solutions Display
<p align="center">
  <img src="docs/images/8queens_multiple_solutions.png" alt="Multiple 8-Queens Solutions" width="700"/>
</p>

### Performance Comparison
<p align="center">
  <img src="docs/images/performance_comparison.png" alt="Algorithm Performance Comparison" width="700"/>
</p>

### Fitness Evolution
<p align="center">
  <img src="docs/images/fitness_evolution.png" alt="Fitness Evolution" width="700"/>
</p>

### Solution Discovery Timeline
<p align="center">
  <img src="docs/images/solution_timeline.png" alt="Solution Timeline" width="700"/>
</p>

</details>

---

## Installation

### Prerequisites
- **Python** 3.11 or higher
- **pip** or **conda** package manager

### Option 1: Install with pip (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd n_queens_problem_python

# Install dependencies
pip install -r requirements.txt

# (Optional) Install in development mode
pip install -e .
```

### Option 2: Install with Conda

```bash
# Clone the repository
git clone <repository-url>
cd n_queens_problem_python

# Create conda environment
conda env create -f JNotebook.yml

# Activate environment
conda activate JNotebook
```

### Verify Installation

```python
python -c "from n_queens import EvolManager, Chromosome, visualization; print('✓ Installation successful!')"
```

---

## Usage

### Running the Genetic Algorithm

```python
from n_queens import EvolManager

# Create evolution manager for 12-Queens problem
evol_manager = EvolManager(
    genes_per_chrom=12,       # Board size (12x12)
    pop=1000,                 # Population size
    generations=50,           # Number of generations
    reproductive_pool_size=800,  # Selection pool size
    offspring=500             # Offspring per generation
)

# Run the genetic algorithm
evol_manager.greedy_evolution()

# Display found solutions
evol_manager.show_solutions()

# Get solutions programmatically
solutions = evol_manager.get_solutions()
print(f"Found {len(solutions)} unique solutions!")
```

### Running Las Vegas Algorithm

```python
# Las Vegas: Random search until solutions found
evol_manager.las_vegas(attempts=500000)

# Show solutions with timestamps
evol_manager.show_solutions()

# Get solution discovery times
times = evol_manager.get_solution_times()
print(f"First solution found in {times[0]:.2f} seconds")
```

### Running Monte Carlo Algorithm

```python
# Monte Carlo: Estimate solution probability
probability = evol_manager.montecarlo(attempts=500000)

print(f"Solution probability: {probability:.6f}")
print(f"Percentage: {probability * 100:.4f}%")
```

### Using Visualizations

```python
from n_queens import Chromosome, visualization
import numpy as np

# Create and visualize a solution
solution = Chromosome(np.array([3, 6, 2, 7, 1, 4, 0, 5]))
visualization.render_board(
    solution.get_positions(),
    title="8-Queens Solution",
    save_path="my_solution.png"
)

# Display multiple solutions in a grid
solutions = evol_manager.get_solutions()
visualization.render_multiple_solutions(
    solutions,
    max_display=6,
    save_path="solutions_grid.png"
)

# Plot fitness evolution over generations
fitness_history = [manager.get_best_chrom_fitness() for gen in range(50)]
visualization.plot_fitness_evolution(
    fitness_history,
    title="Genetic Algorithm Convergence",
    save_path="convergence.png"
)

# Compare algorithm performance
visualization.plot_performance_comparison(
    algorithms=['Genetic', 'Las Vegas', 'Monte Carlo'],
    times=[15.2, 82.1, 90.3],
    solutions_found=[35, 18, 14],
    save_path="comparison.png"
)
```

---

## Algorithms

### 1. Genetic Algorithm (Greedy Evolution)

**How it works:**
1. Initialize random population of chromosomes
2. Evaluate fitness of each chromosome
3. Select best chromosomes for reproduction
4. Generate offspring through mutation (swap operation)
5. Replace population with best individuals (elitism)
6. Repeat for specified generations

**Best for:** Finding multiple diverse solutions efficiently

**Parameters:**
- `genes_per_chrom`: Board size (N)
- `pop`: Population size (recommended: 500-1000 for N=12)
- `generations`: Evolution cycles (50-100 typical)
- `reproductive_pool_size`: Selection pool (default: 80% of population)
- `offspring`: Children per generation (default: 1.5× pool size)

### 2. Las Vegas Algorithm

**How it works:**
1. Generate random board configurations
2. Check if configuration is a valid solution
3. If valid, save it; otherwise, repeat
4. Continue until desired number of solutions found

**Best for:** Guaranteed correctness, simple implementation

**Trade-offs:** Unpredictable runtime, slower for larger N

### 3. Monte Carlo Algorithm

**How it works:**
1. Generate fixed number of random configurations
2. Count how many are valid solutions
3. Calculate probability = solutions / total attempts

**Best for:** Understanding problem difficulty, probability estimation

**Trade-offs:** Doesn't guarantee finding solutions, statistical only

---

## Project Structure

```
n_queens_problem_python/
│
├── src/n_queens/              # Core package
│   ├── __init__.py           # Package initialization
│   ├── chromosome.py         # Chromosome class with permutation encoding
│   ├── evolution_manager.py  # Algorithm implementations
│   └── visualization.py      # Plotting and rendering utilities
│
├── notebooks/                 # Interactive demonstrations
│   ├── 01_chromosome_demo.ipynb         # Chromosome usage examples
│   ├── 02_algorithm_comparison.ipynb    # Benchmark comparisons
│   └── 03_statistical_analysis.ipynb    # Convergence analysis
│
├── docs/images/              # Documentation assets
│   ├── 8queens_solution.png
│   ├── 8queens_multiple_solutions.png
│   ├── performance_comparison.png
│   └── ...
│
├── tests/                    # Unit tests (future)
├── data/                     # Experimental data
│   ├── raw/                  # Original data
│   └── processed/            # Cleaned data
├── results/                  # Output figures and files
│
├── generate_visualizations.py  # Script to create doc images
├── requirements.txt          # Python dependencies
├── JNotebook.yml            # Conda environment specification
├── .gitignore               # Git ignore patterns
└── README.md                # This file
```

### Key Components

#### 📦 **Chromosome Class** (`src/n_queens/chromosome.py`)
Represents a board configuration using permutation encoding.

**Key Methods:**
- `fitness()` → float - Evaluates solution quality (0.0-1.0)
- `mutual_threats()` → int - Counts diagonal conflicts
- `make_child()` → Chromosome - Creates mutated offspring
- `random_vec()` → ndarray - Generates random configuration

#### 🧮 **EvolManager Class** (`src/n_queens/evolution_manager.py`)
Orchestrates all three algorithmic approaches.

**Key Methods:**
- `greedy_evolution()` - Run genetic algorithm
- `las_vegas(attempts)` - Run Las Vegas algorithm
- `montecarlo(attempts)` - Run Monte Carlo estimation
- `get_solutions()` - Retrieve found solutions
- `show_solutions()` - Display solutions with metadata

#### 🎨 **Visualization Module** (`src/n_queens/visualization.py`)
Professional plotting and rendering utilities.

**Key Functions:**
- `render_board()` - Single board with queen symbols
- `render_multiple_solutions()` - Grid of solutions
- `plot_fitness_evolution()` - Convergence chart
- `plot_performance_comparison()` - Algorithm benchmarks
- `plot_solution_distribution()` - Discovery timeline

---

## Results & Performance

### Genetic Algorithm Performance

**Configuration:** N=12, Population=1000, Generations=50

| Metric | Value |
|--------|-------|
| **Solutions Found** | ~35 unique solutions |
| **Time to First Solution** | 3-4 seconds |
| **First Solution Generation** | 9-15 |
| **Total Runtime** | 15-20 seconds |
| **Success Rate** | 100% |

### Algorithm Comparison (N=12)

| Algorithm | Solutions | Time (s) | Pros | Cons |
|-----------|-----------|----------|------|------|
| **Genetic** | 35 | 15.2 | Fast, many solutions | Requires tuning |
| **Las Vegas** | 18 | 82.1 | Simple, guaranteed | Slower, unpredictable |
| **Monte Carlo** | N/A | 90.3 | Probability estimate | No actual solutions |

### Scalability

| Board Size (N) | Genetic (50 gen) | Las Vegas (100k) | Difficulty |
|----------------|------------------|------------------|------------|
| 8 | ~2 sec | ~5 sec | Easy |
| 10 | ~8 sec | ~25 sec | Medium |
| 12 | ~15 sec | ~80 sec | Hard |
| 16 | ~45 sec | ~300 sec | Very Hard |

---

## Examples & Notebooks

Explore the [notebooks/](notebooks/) directory for interactive demonstrations:

### 📓 [01_chromosome_demo.ipynb](notebooks/01_chromosome_demo.ipynb)
- Chromosome class usage
- Permutation encoding explanation
- Mutation and fitness evaluation
- Visual board representations

### 📊 [02_algorithm_comparison.ipynb](notebooks/02_algorithm_comparison.ipynb)
- Side-by-side algorithm comparison
- Performance benchmarking
- Solution quality analysis
- Visual comparisons

### 📈 [03_statistical_analysis.ipynb](notebooks/03_statistical_analysis.ipynb)
- Population fitness distributions
- Convergence analysis
- Multi-board size comparisons
- Statistical insights

**To run notebooks:**
```bash
jupyter notebook notebooks/
```

---

## Configuration

### Genetic Algorithm Tuning

```python
# Fast exploration (quick results)
EvolManager(genes_per_chrom=8, pop=100, generations=20)

# Balanced (recommended for N=12)
EvolManager(genes_per_chrom=12, pop=1000, generations=50)

# Thorough search (maximum diversity)
EvolManager(
    genes_per_chrom=12,
    pop=2000,
    generations=100,
    reproductive_pool_size=1600,
    offspring=800
)
```

### Parameter Guidelines

| Parameter | Small N (≤8) | Medium N (10-12) | Large N (≥14) |
|-----------|--------------|------------------|---------------|
| `pop` | 100-500 | 500-1000 | 1000-2000 |
| `generations` | 20-30 | 50-100 | 100-200 |
| `reproductive_pool_size` | 80-400 | 400-800 | 800-1600 |
| `offspring` | 100-500 | 500-1000 | 1000-2000 |

---

## Troubleshooting

### Common Issues

**Q: Import error: "No module named 'n_queens'"**
A: Make sure you're in the project directory and have installed dependencies:
```bash
pip install -r requirements.txt
```

**Q: "np.float_ was removed" error**
A: Update NumPy to version 2.0+:
```bash
pip install --upgrade numpy
```

**Q: Visualizations not displaying in notebooks**
A: Add `%matplotlib inline` at the top of your notebook:
```python
%matplotlib inline
import matplotlib.pyplot as plt
```

**Q: Genetic algorithm not finding solutions**
A: Try increasing population size and generations:
```python
EvolManager(genes_per_chrom=N, pop=1000, generations=100)
```

**Q: Memory issues with large populations**
A: Reduce population size or use smaller board sizes:
```python
EvolManager(genes_per_chrom=12, pop=500, generations=100)
```

---

## Contributing

Contributions are welcome! Here's how you can help:

### Areas for Improvement
- 🧪 **Unit tests** - Add comprehensive test coverage
- ⚡ **Performance** - Implement parallel processing
- 🎯 **Algorithms** - Add simulated annealing, hill climbing
- 🖥️ **Interface** - Create GUI or web interface
- 📝 **Documentation** - Expand tutorials and examples
- 🐛 **Bug fixes** - Report and fix issues

### Development Setup

```bash
# Fork and clone your fork
git clone https://github.com/your-username/n_queens_problem_python
cd n_queens_problem_python

# Create development branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Make your changes and commit
git add .
git commit -m "Description of changes"

# Push and create pull request
git push origin feature/your-feature-name
```

### Coding Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write Google-style docstrings
- Include examples in docstrings
- Update tests for new features

---

## License

This project is open source. Please specify your license terms.

**Suggested licenses:**
- [MIT License](https://opensource.org/licenses/MIT) - Permissive, simple
- [Apache 2.0](https://opensource.org/licenses/Apache-2.0) - Patent protection
- [GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html) - Copyleft

---

## Authors

**Project Maintainer:** [Your Name]

**Contributors:** See [GitHub Contributors](https://github.com/your-repo/graphs/contributors)

---

## Acknowledgments

- Based on classical N-Queens problem formulations
- Inspired by evolutionary computation research
- Uses modern Python best practices and type safety

---

## References

### Academic Papers
- **N-Queens Problem**
  Wikipedia: https://en.wikipedia.org/wiki/Eight_queens_puzzle

- **Genetic Algorithms**
  Wikipedia: https://en.wikipedia.org/wiki/Genetic_algorithm
  Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization and Machine Learning*

- **Evolutionary Computation**
  Eiben, A. E., & Smith, J. E. (2003). *Introduction to Evolutionary Computing*

### Useful Resources
- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)

---

<p align="center">
  <sub>Built with ❤️ using Python, NumPy, and Matplotlib</sub>
</p>

<p align="center">
  <sub>If you find this project helpful, please consider giving it a ⭐ on GitHub!</sub>
</p>

*This project has been created as part of the 42 curriculum by **jbordeli** and **ajeloyan**.*

# A-Maze-ing

A terminal-based **maze generator, solver, and visualizer** written in Python.

---

## Table of Contents

1. Overview  
2. Features  
3. Installation  
4. Configuration  
5. Usage  
6. Interactive Menu  
7. Algorithms  
8. Project Management  
9. Tools Used  
10. AI Usage  
11. Resources  

---

# Overview

**A-Maze-ing** is a Python project developed as part of the **42 curriculum**.

The goal of the project was to design a complete maze engine capable of:

- Procedurally generating mazes  
- Displaying them directly in the terminal  
- Solving them automatically  
- Exporting them to a file  
- Validating user configuration inputs  

This project combines several important programming concepts:

- Object-Oriented Programming  
- Graph algorithms  
- Pathfinding  
- Input validation  
- Terminal rendering  

The entire application is fully interactive through a terminal menu system.

---

# Features

## Maze Generation

Generate mazes using two different algorithms:

- **DFS (Depth First Search)**
- **Kruskal**

## Maze Types

Choose between:

- **Perfect Maze** → only one valid path between two cells  
- **Imperfect Maze** → loops and multiple possible paths  

## Maze Solver

Automatic path solving using **BFS (Breadth First Search)**.

## Terminal Interface

Interactive menu allowing users to:

- Generate a new maze  
- Show / hide the solution path  
- Change generation algorithm  
- Change colors  
- Enable / disable animation  
- Switch between perfect / imperfect mode  

## Export

Generated mazes can be exported to a `.txt` file.

## Reproducibility

Use an optional **SEED** value to generate the same maze again.

---

# Installation

## Requirements

- Python **3.10+**
- Poetry

## Install Dependencies

```bash
make install
```

## Configuration

Before launching the program, define the maze settings inside the config.txt file.

You can configure:

Maze width and height
Entry and exit positions
Perfect or imperfect maze mode
Colors for walls, paths, and special cells
Optional SEED for deterministic generation
Example 
```txt
WIDTH=20
HEIGHT=20
ENTRY=1,1
EXIT=15,15
OUTPUT_FILE=maze.txt
PERFECT=False
WALL_COLOR=MULTI
PATH_COLOR=CYAN
SPEC_COLOR=PURPLE
SEED=42
```

## Available colors:
### ORANGE, SALMON, GREEN, CYAN, PURPLE, WHITE, MULTI


## Usage

Run the program with:
```bash
make run
```
# Interactive Menu

The program includes a fully interactive terminal menu that allows users to control maze generation in real time.

Once launched, the menu displays the current maze directly in the terminal along with all available actions.

### Users can:

Generate a new maze instantly
Show or hide the solved path
Switch between DFS and Kruskal algorithms
Enable or disable animation
Toggle between perfect and imperfect mazes
Customize wall colors using several presets


All modifications are applied immediately, providing direct visual feedback in the terminal.

This system makes the project intuitive, dynamic, and enjoyable to explore.

Algorithms
DFS — Depth First Search

A recursive backtracking algorithm used to generate long and organic maze paths.

Kruskal

A graph-based algorithm using disjoint sets to create balanced and structured mazes.

BFS — Breadth First Search

Used to automatically solve the maze and find the shortest valid path.

Why These Algorithms

We selected these algorithms because they offer complementary strengths:

DFS produces more natural and winding mazes
Kruskal creates more uniform structures
BFS guarantees the shortest path solution

This combination allows both variety and efficiency.

# Project Management

The workload was naturally shared between both team members throughout the project.

From the beginning, we both wanted to explore different aspects of the codebase and gain experience across multiple components of the application. As a result, each team member proposed and implemented a different maze generation algorithm.

Ajeloyan focused on the visual side of the project, including maze rendering and the menu interface.
Jbordeli designed the maze-solving algorithm and handled the output generation system.

Collaboration went smoothly during the entire development process.

At first, we worked on separate branches within a shared GitHub repository, allowing independent progress while keeping the codebase organized.

Later, once the project structure was stable and we had more opportunities to work side by side, most development continued directly on the main branch.

This workflow proved efficient and helped maintain strong coordination throughout the project.

### Tools Used
Python 3.10
Poetry
Git / GitHub
Makefile
Terminal ANSI Colors
AI Usage

AI tools were used as assistance for:

Documentation drafting
English wording improvements

All design, implementation, debugging, and project decisions were made by the team.

Resources
Python Documentation
Poetry Documentation
Maze Generation Research Articles

# Amazeing Generator - User Guide

## Overview

**Amazeing Generator** is a standalone Python maze generator.

It creates grid-based mazes, solves them automatically, and exports the result into a text file.

This version is intended for users who only have access to:

* `generator.py`

You do **not** need `validator.py`.

All settings are passed directly through a Python dictionary.

---

# What the Program Does

The generator can:

* Create random mazes
* Use different generation algorithms
* Solve the maze automatically
* Save the maze data to a `.txt` file
* Use colored terminal rendering (optional)

---

# Maze Generation Algorithms

## DFS (Depth-First Search)

A classic recursive-backtracking style maze generator.

### Characteristics:

* Long corridors
* Deep paths
* Natural looking mazes
* Fast generation

Use:

```python
maze.dfs_generation()
```

---

## Kruskal Algorithm

Builds the maze by progressively connecting cells.

### Characteristics:

* More balanced structure
* Many branches
* Good distribution

Use:

```python
maze.kruskal_generation()
```

---

# Required Python Version

Python 3.10+

---

# Basic Project Structure

```text
project/
├── generator.py
└── main.py
```

---

# How to Write main.py

## Example

```python
from mazegen.generator import MazeGenerator, Colors

config = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (19, 14),
    "OUTPUT_FILE": "maze.txt",

    "PERFECT": True,
    "WALL_COLOR": Colors.MULTI,
    "PATH_COLOR": Colors.CYAN,
    "SPEC_COLOR": Colors.PURPLE,

    "SEED": 42
}

maze = MazeGenerator(config)

maze.dfs_generation()
```

Run with:

```bash
python main.py
```

---

# Configuration Options

## Required Keys

| Key         | Type  | Description             |
| ----------- | ----- | ----------------------- |
| WIDTH       | int   | Maze width              |
| HEIGHT      | int   | Maze height             |
| ENTRY       | tuple | Start position `(x, y)` |
| EXIT        | tuple | Exit position `(x, y)`  |
| OUTPUT_FILE | str   | Output filename         |

---

## Optional Keys

| Key        | Default | Description          |
| ---------- | ------- | -------------------- |
| PERFECT    | True    | Unique solution maze |
| WALL_COLOR | MULTI   | Wall color           |
| PATH_COLOR | CYAN    | Solved path color    |
| SPEC_COLOR | PURPLE  | Entry/Exit color     |
| SEED       | None    | Random seed          |

---

# Example Configurations

## Small Maze

```python
config = {
    "WIDTH": 10,
    "HEIGHT": 10,
    "ENTRY": (0, 0),
    "EXIT": (9, 9),
    "OUTPUT_FILE": "small.txt"
}
```

---

## Large Maze

```python
config = {
    "WIDTH": 40,
    "HEIGHT": 25,
    "ENTRY": (0, 0),
    "EXIT": (39, 24),
    "OUTPUT_FILE": "large.txt",
    "SEED": 7
}
```

---

# Colors Available

Use:

```python
Colors.ORANGE
Colors.SALMON
Colors.GREEN
Colors.CYAN
Colors.PURPLE
Colors.WHITE
Colors.MULTI
```

Example:

```python
"WALL_COLOR": Colors.GREEN
```

---

# Output File Format

The generated `.txt` file contains:

1. Maze hexadecimal wall encoding
2. Entry coordinates
3. Exit coordinates
4. Solution path directions

Example:

```text
C4A3F...
0,0
19,14
EESSENNWW...
```

---

# Important Notes

## Coordinates

Coordinates are zero-based:

Top-left cell:

```python
(0, 0)
```

Bottom-right for width=20 height=15:

```python
(19, 14)
```

---

## Entry and Exit Must Be Inside the Grid

Correct:

```python
ENTRY = (0, 0)
EXIT = (19, 14)
```

Wrong:

```python
EXIT = (20, 15)
```

---

# Reproducible Mazes

Use `SEED`:

```python
"SEED": 42
```

Same seed = same maze.

---

# Full Example

```python
from mazegen.generator import MazeGenerator, Colors

config = {
    "WIDTH": 30,
    "HEIGHT": 20,
    "ENTRY": (0, 0),
    "EXIT": (29, 19),
    "OUTPUT_FILE": "result.txt",
    "PERFECT": True,
    "WALL_COLOR": Colors.MULTI,
    "PATH_COLOR": Colors.GREEN,
    "SPEC_COLOR": Colors.ORANGE,
    "SEED": 123
}

maze = MazeGenerator(config)

maze.kruskal_generation()
```

---

# Troubleshooting

## File Not Created

Check:

* `OUTPUT_FILE` name is valid
* Write permissions
* Program completed normally

---

## Wrong Coordinates

Make sure:

```python
0 <= x < WIDTH
0 <= y < HEIGHT
```

---

## Colors Not Working

ANSI colors depend on terminal support.

Use modern terminals:

* Windows Terminal
* iTerm2
* GNOME Terminal
* VS Code Terminal

---

# Summary

Minimal usage:

```python
from generator import MazeGenerator

maze = MazeGenerator({
    "WIDTH": 10,
    "HEIGHT": 10,
    "ENTRY": (0, 0),
    "EXIT": (9, 9),
    "OUTPUT_FILE": "maze.txt"
})

maze.dfs_generation()
```

---

Enjoy generating mazes.

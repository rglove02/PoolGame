# PoolGame - Billiards Physics & Web Application
A C and Python-based physics engine and webserver for simulating and interacting with a game of billiards.

This repository contains my work for Assignments 1–4 of CIS*2750 at the University of Guelph, including:
- A C physics engine for simulating pool ball motion and collisions (`phylib`)
- A Python interface for visualization and simulation
- A database backend to track games, players, and shots
- A web-based interactive 8-ball game using SVGs and Python’s HTTPServer

## Features

### Assignment 1: Billiards Physics Library in C
- Implements 2D vector operations and ball dynamics
- Simulates collisions between balls, cushions, and holes
- Provides physics simulation with velocity, acceleration, drag, and collision detection
- Modular design using polymorphic structs in pure C
- Fully compiled as a shared library (`libphylib.so`)
- Includes `Makefile` for clean builds using `clang -std=c99 -Wall -pedantic`

### Assignment 2: Python Web Server with SVG Output
- Exposes the C physics library to Python using SWIG
- Defines Python classes (`RollingBall`, `StillBall`, `Hole`, `Cushion`, `VCushion`, `Table`) that wrap C structs
- Exports billiards tables as SVG files for rendering in browsers
- Simple Python webserver using `http.server` to process user input and return SVG-based simulations
- Supports POST requests to animate ball movement in browser

### Assignment 3: Pool Physics SQL Database
- Adds persistent storage for pool tables and game shots using SQLite3
- `Physics.py` extended with:
  - `Database` class for read/write operations
  - `Game` class for game-level control and shot simulation
- Maps objects to `Ball`, `TTable`, `BallTable`, `Shot`, `TableShot`, `Player`, and `Game` tables
- Enables saving and restoring game states across sessions

### Assignment 4: Interactive 8-Ball Game
- Full SVG-based 8-ball gameplay in browser
- Click and drag on cue ball to simulate shots
- Animates table state based on database contents
- Tracks player turns, assigns high/low groups based on first sunk ball
- Determines game winner based on valid 8-ball rules
- All game logic runs in Python with frontend rendered via dynamic SVG

## Setup/Run Instructions

### Compilation (C Components)
Run the following on SoCS servers:
```bash
make
```

### Testing:
```
python3 A2Test1.py       # Basic ball motion test
python3 A2Test2.py       # Generates SVG outputs
```

### Play the game:
```
python3 server.py 5XXXX  # Launch local web server (use last 4 digits of student ID)
http://localhost:5XXXX/shoot.html
```

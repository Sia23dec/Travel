# Optimized Route Finder

A Python project that uses the A* Search algorithm to find optimal delivery routes in an urban environment simulation.

## Project Structure

OptimizedRouteFinder/
├── images/ # Folder for saving visualization plots
├── main.py # Main program code
├── report.docx # Project report (or .md)
├── requirements.txt # Python dependencies
└── README.md # This file

## Setup Instructions

### 1. Create and Activate Virtual Environment

Navigate to the project folder and run:

```bash
# Create the environment
python -m venv venv

# Activate on Mac/Linux
source venv/bin/activate

# Activate on Windows
.\venv\Scripts\activate
```

### 2. Install Required Packages

With the environment active, run:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install networkx matplotlib
```

### 3. Run the Program

```bash
python main.py
```

The program will:

- Display Scenario 1 results in the terminal and show a plot.
- Display Scenario 2 results and show a second plot.
- You should save the plots manually into the images/ folder for your report.

## Usage

The program demonstrates two key scenarios:

1. **Normal Traffic**: Finds the optimal path from the 'Warehouse' to location 'G'.
2. **Traffic Jam**: Simulates a traffic jam on a critical road and shows how the algorithm finds a new, optimal route.

## Author

**Name:** Sia Mishra  
**Roll Number:** 2309659

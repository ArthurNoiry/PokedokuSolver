
# Tutorial: Pokédoku Puzzle Search with SQLite and Pandas

This tutorial will guide you through a Python program that searches for Pokémon based on specific conditions to solve a 3x3 Pokédoku puzzle. The program uses an SQLite database in memory and reads data from an Excel file using the `pandas` library. You can customize the search conditions based on Pokémon types, regions, evolutionary stages, and other attributes.

## Prerequisites

To run this program, you need to install the following Python packages:

- `sqlite3` (included in the standard Python library)
- `pandas` (for data manipulation)

You can install `pandas` with the following command if you don't have it already:

```bash
pip install pandas
```

## Code Overview

The code consists of several key sections:

1. **Logging Setup**
2. **Loading Data from Excel**
3. **Query Construction**
4. **Search Function**
5. **Results Display**

### 1. Logging Setup

First, we set up logging to track errors and important information during execution.

```python
import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    filename='application.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### 2. Loading Data from Excel

We load Pokémon data from an Excel file (`database.xlsx`). This file should contain a sheet called "pokemon" with columns such as `Name`, `Type1`, `Type2`, `Region`, etc.

```python
df = pd.read_excel("database.xlsx", sheet_name="pokemon")
```

Then, we create an SQLite in-memory database and store the DataFrame in it as a table.

```python
conn = sqlite3.connect(":memory:")
df.to_sql("table_excel", conn, index=False, if_exists="replace")
```

### 3. Query Construction

The main search logic is built around SQL queries that filter Pokémon based on conditions provided in the function call. The conditions could include:

- Pokémon type (e.g., "TypeFire", "TypeWater")
- Evolutionary stage (e.g., "Evolution1", "Evolution2")
- Region (e.g., "RegionKanto")

### 4. Search Function: `recherche()`

This function takes two arguments:

- `conditions_colonne`: Conditions for filtering columns.
- `conditions_ligne`: Conditions for filtering rows.
- `Grid`: If `True`, it prints a 3x3 grid with Pokémon names based on the search.

Here’s the core function:

```python
def recherche(conditions_colonne=["TypeNormal"], conditions_ligne=["Mono"], Grid=False):
    # Load the data
    df = pd.read_excel("database.xlsx", sheet_name="pokemon")

    # Create an in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    df.to_sql("table_excel", conn, index=False, if_exists="replace")

    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for condition_colonne in conditions_colonne:
        for condition_ligne in conditions_ligne:
            query = "SELECT * FROM table_excel WHERE "
            # Add conditions to the query
            # ... (condition parsing code)
            result = pd.read_sql_query(query, conn)
            
            # Filter and prioritize results
            # ... (result prioritization code)
            
            # Update the grid with results
            for name in prioritized_result['Name']:
                if name not in [grid[x][y] for x in range(3) for y in range(3)]:
                    grid[j][i] = name
                    break
            
            if not Grid:
                print(", ".join(top_5['Name'].tolist()))

    if Grid:
        print("\nGrid:")
        for row in grid:
            print("\t".join(row))
    conn.close()
```

### 5. Results Display

- If `Grid=False`, the program will print the top Pokémon matching the search criteria.
- If `Grid=True`, the program will output a 3x3 grid with the selected Pokémon names.

### Example Function Call

Here’s an example of how to call the `recherche()` function:

```python
recherche(["TypePsychic", "TypeMono", "BoolStarter"], ["RegionSinnoh", "TypeFire", "RegionUnova"], Grid=True)
```

This will search for Pokémon of type "Psychic", mono-type Pokémon, and starter Pokémon, located in the "Sinnoh" or "Unova" regions, and it will display the results in a 3x3 grid.

---

## Conclusion

This program is useful for solving a Pokédoku puzzle, where you need to place Pokémon in a 3x3 grid based on specific conditions. By leveraging SQLite and Pandas, the program efficiently searches for Pokémon matching multiple criteria and prioritizes the results accordingly.

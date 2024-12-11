# Project description
This project is aimed at solving a [Pokedoku](https://pokedoku.com/) grid as per it's rules that could be summarized as such :
a 3x3 grid has 6 criteria, one for each columns and rows, in each cell the player must put a Pokemon that matches both the criteria from it's column and row

to use it simply execute the .py file and then type
```bash
recherche(["Column1","Column2","Column3"],["Row1","Row2","Row3"])
```
With "Column1","Column2","Column3","Row1","Row2","Row3" being the criteria of the grid put in the following format :
for a specific type : "Type"+Type name(capitalized)
for either Mono or Dual Type : "Type"+"Mono" or "Dual"
Specific stage of evolution : "Evolution"+1,2,3 or -1 for respectively first stage, middle stage, final stage and no evolution line
Region of origin : "Region"+Region name(capitalized)
a specific group of pokemon (Baby, Legendary, Evolve from an Item) : "Bool"+Name of column in the database
currently the boolean columns are :
Legendary, Baby, Fossil, Mythical, Paradox, Starter, Ultra-Beast, Mega, Gmax, Branched, Friendship, Item, Trade
If you encounter an ability or move as a condition it is also "Bool"+name but for the few that have spaces, replace them with underscores

# Project Setup Instructions
The following instructions are here in case you want to setup the project to contribute to it, if you just want to use it you do not have to follow them
## 1. Static Code Analysis with Flake8

### **Step 1: Install Flake8**
To enable static code analysis for Python, install Flake8 using pip:
```bash
pip install flake8
```

### **Step 2: Create a Flake8 Configuration File**
In the root directory of your project, create a `.flake8` configuration file with the following content:
```ini
[flake8]
max-line-length = 88
ignore = E203, E266, E501, W503
```
This configuration enforces a maximum line length of 88 characters and ignores certain stylistic warnings.

### **Step 3: Run Flake8 Analysis**
To run Flake8 on a specific file, navigate to your project directory and execute:
```bash
flake8 <filename>
```
For example, to analyze `recherche.py`:
```bash
flake8 ~/software/recherche.py
```

Flake8 will output any violations it finds along with the line numbers and error codes.

---

## 2. Automate Static Code Analysis with Pre-commit Hooks

### **Step 1: Install Pre-commit**
Install the `pre-commit` framework using pip:
```bash
pip install pre-commit
```

### **Step 2: Create a Pre-commit Configuration File**
In the root directory of your project, create a `.pre-commit-config.yaml` file with the following content:
```yaml
repos:
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0  # Use the latest version
    hooks:
      - id: flake8
```
This configuration sets up Flake8 as a pre-commit hook.

### **Step 3: Install Pre-commit Hooks**
Install the hooks into your local Git repository:
```bash
pre-commit install
```
This command creates the necessary Git hooks to run Flake8 before every commit.

### **Step 4: Run Pre-commit Hooks**
To test the hooks on all files in your repository, use:
```bash
pre-commit run --all-files
```

### **Step 5: Commit Changes**
Once the hooks are installed, every `git commit` will automatically run Flake8 checks on staged files. If any violations are found, the commit will fail, and you'll need to fix the issues before committing again.

---

### Troubleshooting
- If you encounter issues with the configuration, ensure the `.pre-commit-config.yaml` and `.flake8` files are present in the root directory of your project.
- Check the pre-commit log at `~/.cache/pre-commit/pre-commit.log` for detailed error messages.

---

### Example
To check your setup, perform the following steps:
1. Modify a Python file (e.g., `recherche.py`) and introduce a coding style error (e.g., a line longer than 88 characters).
2. Stage the file:
   ```bash
   git add recherche.py
   ```
3. Commit the file:
   ```bash
   git commit -m "Test pre-commit hook"
   ```
   If the hook detects a violation, the commit will fail, and you'll see the Flake8 error message.

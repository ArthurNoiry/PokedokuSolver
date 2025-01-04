import sqlite3
import pandas as pd
import logging
logging.basicConfig(
    filename='application.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


'''#  Charger les données Excel
df = pd.read_excel("database.xlsx", sheet_name="pokemon")

#  Créer une base SQLite en mémoire
conn = sqlite3.connect(":memory:")
df.to_sql("table_excel", conn, index=False, if_exists="replace")
query = "SELECT Name FROM table_excel WHERE "
#  Requête SQL
name = "Pikachu"
query = "SELECT Name, Legendary FROM table_excel WHERE Name = ?"
result = pd.read_sql_query(query, conn, params=(name, ))
print(result)
conn.close()'''


def recherche(conditions_colonne=["TypeNormal"], conditions_ligne=["Mono"], Grid=False):
    """
    This program aims to find all possible solutions for any square in a Pokédoku puzzle.
    The game is presented as a 3x3 grid, where each row and column has a condition for which Pokémon can be placed.
    To achieve this, it uses a database containing all the information required for Pokédoku.
    Columns:
    #, Name, Type1, Type2, Generation, Legendary, Baby, Fossil, Mythical, Paradox,
    Starter, Ultra-Beast, Mega, Gmax, Evolution, Branched, Friendship, Item,
    Trade, Region, Intimidate, Keen_Eye, Levitate, Sturdy, Swift_Swim, Close_Combat,
    Crunch, Dazzling_Gleam, Earthquake, Flamethrower, Fly, Hydro_Pump, Ice_Beam,
    Psychic, Razor_Leaf, Shadow_Ball, Thunderbolt
    List of queries, note that the program will not check if the parameter of
    the query is valid, this is voluntary to add more modularity to the database
    Type+param : searches for the pokemons of the given param type
        exceptions : Mono searches for it has only one type and Dual for
        the ones that have two
    
    """
    #  Charger les données Excel
    df = pd.read_excel("database.xlsx", sheet_name="pokemon")

    #  Créer une base SQLite en mémoire
    conn = sqlite3.connect(":memory:")
    df.to_sql("table_excel", conn, index=False, if_exists="replace")
    i = -1
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    no_result=False
    for condition_colonne in conditions_colonne:
        i += 1
        j = -1
        for condition_ligne in conditions_ligne:
            j += 1
            query = "SELECT * FROM table_excel WHERE "
            # ajout de la première condition
            if (condition_colonne.startswith("Type")):
                param = "'"+condition_colonne[4:]+"'"
                if (param == "'Mono'"):
                    query = query + "Type2 IS NULL AND "
                elif (param == "'Dual'"):
                    query = query + "Type2 IS NOT NULL AND "
                else:
                    query = query + f"(Type1={param} OR Type2={param}) AND "
            elif (condition_colonne.startswith("Bool")):
                param = condition_colonne[4:]
                query = query + f"{param}=1 AND "
            elif (condition_colonne.startswith("Region")):
                param = "'"+condition_colonne[6:]+"'"
                query = query + f"Region={param} AND "
            elif (condition_colonne.startswith("Evolution")):
                param = int(condition_colonne[9:])
                query = query + f"Evolution={param} AND "
            else:
                print(f"erreur, {condition_colonne} argument invalide")
                return 1
            # ajout de la deuxième condition
            if (condition_ligne.startswith("Type")):
                param = "'"+condition_ligne[4:]+"'"
                if (param == "'Mono'"):
                    query = query + "Type2 IS NULL"
                elif (param == "'Dual'"):
                    query = query + "Type2 IS NOT NULL"
                else:
                    query = query + f"(Type1={param} OR Type2={param})"
            elif (condition_ligne.startswith("Bool")):
                param = condition_ligne[4:]
                query = query + f"{param}=1"
            elif (condition_ligne.startswith("Region")):
                param = "'"+condition_ligne[6:]+"'"
                query = query + f"Region={param}"
            elif (condition_ligne.startswith("Evolution")):
                param = int(condition_ligne[9:])
                query = query + f"Evolution={param}"
            else:
                print(f"erreur, {condition_ligne} argument invalide")
                return 1
            print("Condition :", condition_colonne, "+", condition_ligne)
            result = pd.read_sql_query(query, conn)
            if result.empty:
                print(f"No results found for the query:{query}")
                logger.error(f"{query} returned none", exc_info=True)
                no_result=True
                continue

            # Filtre les résultats pour afficher en priorité ceux qui ne sont pas dans le pokédex
            if 'Pokedex' in result.columns:
                if (result['Pokedex'] == False).any():
                    filtered_result = result[result['Pokedex'] == False].copy()
                    filtered_result['Priority'] = (filtered_result['Region'] == 'Unova').astype(int)
                    prioritized_result = filtered_result.sort_values(by='Priority', ascending=False)
                else:
                    print("Every result in pokedex")
                    result = result.copy()
                    result['Priority'] = (result['Region'] == 'Unova').astype(int)
                    prioritized_result = result.sort_values(by='Priority', ascending=False)
            else:
                result = result.copy()
                result['Priority'] = (result['Region'] == 'Unova').astype(int)
                prioritized_result = result.sort_values(by='Priority', ascending=False)
            if result['Name'].str.startswith("Goomy").any():
                print("Goomy trouvé")
            if result['Name'].str.startswith("Sliggoo").any():
                print("Sliggoo trouvé")
            if result['Name'].str.startswith("Goodra").any():
                print("Goodra trouvé")
            top_5 = prioritized_result.head(2)

            for name in prioritized_result['Name']:
                if name not in [grid[x][y] for x in range(3) for y in range(3)]:
                    grid[j][i] = name
                    break
            if not Grid:
                print(", ".join(top_5['Name'].tolist()))
                print()

    if Grid:
        print("\nGrid:")
        for row in grid:
            print("\t".join(map(str, row)))
    conn.close()
    if(no_result):
        return 1
    else:
        return 0

# Exemple d'appel :
recherche(["TypePsychic", "TypeMono", "BoolStarter"], ["RegionSinnoh", "TypeFire", "RegionUnova"], Grid=True)

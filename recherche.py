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
# ce programme cherche à trouver toute les solutions possibles à n'importe quelle case de pokédoku
# ce jeu se présente comme une grille de 3x3 dans laquelle chaque ligne
# et chaque colonne a une condition sur quel pokémon mettre
# pour celà il utilise une database qui contiens toutes les informations demandable par pokédoku
# Collones : #  Name Type1 Type2 Generation Legendary Baby Fossil Mythical
# Paradox Starter Ultra-Beast Mega Gmax Evolution Branched Friendship Item Trade Region
# Intimidate Keen_Eye Levitate Sturdy Swift_Swim Close_Combat Crunch Dazzling_Gleam Earthquake
# Flamethrower Fly Hydro_Pump Ice_Beam Psychic Razor_Leaf Shadow_Ball Thunderbolt


def perform_query(query, table):
    try:
        logger.info(f"Executing query: {query} on the table")
        result = pd.read_sql_query(query, table)
        logger.debug(f"Query result: {result}")
        return result
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise


def recherche(conditions_colonne=["TypeNormal"], conditions_ligne=["Mono"], Grid=False):
    #  Charger les données Excel
    df = pd.read_excel("database.xlsx", sheet_name="pokemon")

    #  Créer une base SQLite en mémoire
    conn = sqlite3.connect(":memory:")
    df.to_sql("table_excel", conn, index=False, if_exists="replace")
    i = -1
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
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
                if param not in conn.columns:
                    logger.error(f"The column {param} is not part of the database")
                    return 1
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
                if param not in conn.columns:
                    logger.error(f"The column {param} is not part of the database")
                    return 1
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
            result = perform_query(query, conn)

            # Filtre les résultats pour afficher en priorité ceux qui ne sont pas dans le pokédex
            if 'Pokedex' in result.columns:
                if (result['Pokedex'] is False).any():
                    filtered_result = result[result['Pokedex'] is False].copy()
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
            print("\t".join(row))
    conn.close()
    return 0

# Exemple d'appel :
# recherche(["BoolItem", "RegionAlola", "RegionPaldea"], ["TypeMono", "TypePoison", "TypeNormal"], Grid=True)

import json, requests, sqlite3

dbconnection = sqlite3.connect('TF2STATS.db')
cursor = dbconnection.cursor()

cursor.execute("""
CREATE TABLE  IF NOT EXISTS MATCHES(
    LogID TEXT PRIMARY KEY,
    Date INTEGER,
    MATCH_LENGTH INTEGER,
    RED_SCORE INTEGER,
    BLU_SCORE INTEGER,
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS MATCH_PLAYERS(

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS MATCH_MEDICS(

)
""")

dbconnection.commit()
dbconnection.close()


            

    
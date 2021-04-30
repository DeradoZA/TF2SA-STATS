import json, requests, sqlite3

def DatabaseStartUp(cursor):

    cursor.execute("""
    CREATE TABLE  IF NOT EXISTS MATCH(
        M_LogID TEXT PRIMARY KEY,
        M_Date INTEGER,
        MATCH_LENGTH INTEGER,
        RED_SCORE INTEGER,
        BLU_SCORE INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MATCH_PLAYER(
        P_SteamID TEXT,
        M_LogID TEXT,
        P_Class_Type TEXT,
        P_Class_Duration INTEGER,
        P_Kills INTEGER,
        P_Assists INTEGER,
        P_Deaths INTEGER,
        P_Damage INTEGER,
        P_Airshots INTEGER,
        P_Headshots INTEGER,
        P_Backstabs INTEGER,
        P_Accuracy REAL,
        PRIMARY KEY (M_LogID, P_SteamID, P_Class_Type)
        FOREIGN KEY (M_LogID)
            REFERENCES MATCH (M_LogID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MATCH_MEDIC(
        P_SteamID TEXT,
        M_LogID TEXT,
        P_Kills INTEGER,
        P_Assists INTEGER,
        P_Deaths INTEGER,
        P_Damage INTEGER,
        P_Airshots INTEGER,
        P_Accuracy REAL,
        P_Class_Duration INTEGER,
        P_Heals INTEGER,
        P_Charges INTEGER,
        P_Drops INTEGER,
        PRIMARY KEY (M_LogID, P_SteamID)
        FOREIGN KEY (M_LogID)
            REFERENCES MATCH (M_LogID)
    )
    """)

if __name__ == "__main__":

    dbconnection = sqlite3.connect('TF2STATS.db')
    cursor = dbconnection.cursor()

    DatabaseStartUp(cursor)

    dbconnection.commit()
    dbconnection.close()


            

    
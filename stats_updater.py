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
        P_Kills INTEGER,
        P_Assists INTEGER,
        P_Deaths INTEGER,
        P_Damage INTEGER,
        P_Airshots INTEGER,
        P_Headshots INTEGER,
        P_Backstabs INTEGER,
        P_Class_Duration INTEGER,
        PRIMARY KEY (M_LogID, P_SteamID, P_Class_Type)
        FOREIGN KEY (M_LogID)
            REFERENCES MATCH (M_LogID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MATCH_MEDIC(
        P_SteamID TEXT,
        M_LogID TEXT,
        P_Class_Type TEXT,
        P_Kills INTEGER,
        P_Assists INTEGER,
        P_Deaths INTEGER,
        P_Damage INTEGER,
        P_Airshots INTEGER,
        P_Drops INTEGER,
        P_Heals INTEGER,
        P_Ubers INTEGER,
        P_Class_Duration INTEGER,
        PRIMARY KEY (M_LogID, P_SteamID)
        FOREIGN KEY (M_LogID)
            REFERENCES MATCH (M_LogID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS WEAPON_STATS(
        P_SteamID TEXT,
        M_LogID TEXT,
        P_Class_Type TEXT,
        P_Weapon_Type TEXT,
        P_Accuracy REAL,
        PRIMARY KEY(P_SteamID, M_LogID, P_Weapon_Type)
        FOREIGN KEY (P_SteamID, M_LogID, P_Class_Type)
            REFERENCES MATCH_PLAYER (M_LogID, P_SteamID, P_Class_Type)
        FOREIGN KEY (P_SteamID, M_LogID, P_Class_Type)
            REFERENCES MATCH_MEDIC (P_SteamID, M_LogID, P_Class_Type)
    )
    """)

if __name__ == "__main__":

    dbconnection = sqlite3.connect('TF2STATS.db')
    cursor = dbconnection.cursor()

    DatabaseStartUp(cursor)

    UploaderFile = open("Uploaders.txt", "r")
    LogsList = []
    LogCount = 0

    for x in UploaderFile:
        
        Uploader = x[11:]
        UploaderLogs = json.loads(requests.get("https://logs.tf/api/v1/log?uploader={}".format(Uploader)).text)

        for x in UploaderLogs["logs"]:
            LogsList.append(x["id"])


    for Log in LogsList:
        Current_log = json.loads(requests.get("http://logs.tf/api/v1/log/{}".format(Log)).text)
        bLogCheck = False
        cursor.execute("SELECT M_LogID FROM MATCH WHERE M_LogID = '{}'".format(Log))
        Log_search = cursor.fetchone()

        if Log_search:
            bLogCheck = True
            print("Match " + str(Log) + " already in system.")
        elif (Current_log["length"] / 60) < 20:
            bLogCheck = True
            print("Match " + str(Log) + " not long enough to be recorded.")

        
        
        if bLogCheck == False:
            LogCount += 1
            print("Updating log " + str(LogCount) + " out of " + str(len(LogsList)) + " - " + str(Log))
            cursor.execute("""
            INSERT INTO MATCH
            VALUES ('{}',{},{},{},{})
            """.format(Log, Current_log["info"]["date"], Current_log["info"]["total_length"], Current_log["teams"]["Red"]["score"], Current_log["teams"]["Blue"]["score"]))

            
            for Player,PlayerStats in Current_log["players"].items():

                Player_team = PlayerStats["team"]
                Player_Airshots = PlayerStats["as"]
                Player_Headshots = PlayerStats["headshots_hit"]
                Player_Backstabs = PlayerStats["backstabs"]

                for Class_stats in PlayerStats["class_stats"]:

                    Class_type = Class_stats["type"]
                    Class_duration = Class_stats["total_time"]
                    Class_kills = Class_stats["kills"]
                    Class_assists = Class_stats["assists"]
                    Class_deaths = Class_stats["deaths"]
                    Class_Damage = Class_stats["dmg"]

                    if Class_type == "medic":
                        Class_Heals = PlayerStats["heal"]
                        Class_Ubers = PlayerStats["ubers"]
                        Class_Drops = PlayerStats["drops"]

                        cursor.execute("""
                        INSERT INTO MATCH_MEDIC
                        VALUES ('{}','{}','{}',{},{},{},{},{},{},{},{},{})
                        """.format(Player, Log, Class_type, Class_kills, Class_assists, Class_deaths, Class_Damage, Player_Airshots, Class_Drops , Class_Heals, Class_Ubers, Class_duration))
                    else:
                        cursor.execute("""
                        INSERT INTO MATCH_PLAYER
                        VALUES ('{}','{}','{}',{},{},{},{},{},{},{},{})
                        """.format(Player, Log, Class_type, Class_kills, Class_assists, Class_deaths, Class_Damage, Player_Airshots, Player_Headshots, Player_Backstabs, Class_duration))

                    for Weapon, WeaponStats in Class_stats["weapon"].items():
                        P_Weapon_Type = Weapon
                        if WeaponStats["shots"] != 0:
                            P_Accuracy = (WeaponStats["hits"] / WeaponStats["shots"]) * 100

                        cursor.execute("""
                        INSERT OR IGNORE INTO WEAPON_STATS
                        VALUES ('{}','{}','{}','{}',{})
                        """.format(Player, Log,Class_type, P_Weapon_Type, P_Accuracy))
                    

    dbconnection.commit()
    dbconnection.close()


            

    
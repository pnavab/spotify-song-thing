import sqlite3
from datetime import datetime, timedelta
import logging


logger = logging.getLogger(__name__)

def maybe_create_table(sqlite_file: str) -> bool:
    db = sqlite3.connect(sqlite_file)
    cursor = db.cursor()

    try :
        create_table_query = """
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY, 
            song_name TEXT NOT NULL, 
            artist_name TEXT NOT NULL, 
            inserted_at DATETIME NOT NULL);
        """

        cursor.execute(create_table_query)
        db.commit()
        return True
    except Exception:
        logger.exception("Unable to create songs table")
        return False
    
def get_number_of_entries(sqlite_file):
    db = sqlite3.connect(sqlite_file)
    cursor = db.cursor()

    count = 0
    try:
        sql = "SELECT COUNT(*) FROM songs"
        cursor.execute(sql)
        result = cursor.fetchone()
        count = result[0]
    except Exception:
        logger.exception("Couldn't get number of songs")
    return count
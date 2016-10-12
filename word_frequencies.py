import sqlite3
import pdb

SENTIMENT = 'a'
DATE = '%Feb 29%'
TABLE = 'climate_2016_03_04'

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

to_execute = "SELECT * FROM " + TABLE + " WHERE date LIKE '" + DATE + "' AND sentiment = '" + SENTIMENT + "'"
print("Query: " + to_execute)
#c.execute(to_execute)

conn.close()

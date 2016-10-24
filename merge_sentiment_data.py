import sqlite3
from util import get_time_mask

table_names, dates = get_time_mask()

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()

for i in range(len(table_names)):
	c.execute("INSERT INTO full_sentiments (text,date,username,location,sentiment) SELECT text,date,username,location,sentiment FROM " + table_names[i] + " WHERE not sentiment='n'")
	print("Adding data from table " + table_names[i])
	conn.commit()
conn.close()

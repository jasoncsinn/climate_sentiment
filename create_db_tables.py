import sqlite3

from util import get_time_mask

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()
table_names, dates = get_time_mask()
#print(len(table_names))
for table_name in table_names:
	to_execute = "CREATE TABLE " + table_name + " (text,date,username,location,sentiment,entropy)"
	print(to_execute)
	c.execute(to_execute)
conn.commit()
conn.close()

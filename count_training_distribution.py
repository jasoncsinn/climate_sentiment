import sqlite3

num_a = 0
num_s = 0
num_o = 0
num_t = 0

conn = sqlite3.connect('data/refined_training_data.db')
c = conn.cursor()
c.execute("SELECT * FROM training")
lines = c.fetchall()
for line in lines:
	text,u_sent,sent = line
	num_t += 1
	if sent == 'a':
		num_a += 1
	if sent == 's':
		num_s += 1
	if sent == 'n':
		num_o += 1

perc_a = 100.0 * num_a / num_t
perc_s = 100.0 * num_s / num_t
perc_o = 100.0 * num_o / num_t

print("num_a: " + str(num_a) + " perc_a: " + str(perc_a))
print("num_s: " + str(num_s) + " perc_s: " + str(perc_s))
print("num_o: " + str(num_o) + " perc_o: " + str(perc_o))
print('total: ' + str(num_t))

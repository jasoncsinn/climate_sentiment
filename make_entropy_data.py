import pdb
import sqlite3
import datetime

import numpy as np

from util import tweet_date
from util import get_time_mask

table_names, dates = get_time_mask()

conn = sqlite3.connect('data/predicted_data.db')
c = conn.cursor()
delta = datetime.timedelta(1)

avg_entropies = []

with open('data/ambiguity_by_sentiment.txt', 'w') as f:
	for i in range(len(table_names)):
		c.execute("SELECT * FROM " + table_names[i])
		db_tweets = c.fetchall()

		cur_date = dates[i]
		end_date = dates[i+1]
		date_mask = []
		while cur_date <= end_date:
			date_mask.append(cur_date)
			cur_date += delta

		for i in range(len(date_mask)):
			tweets = [t for t in db_tweets if tweet_date(t[1]) == date_mask[i]]
			a_entropies = [float(t[5]) for t in tweets if t[4] == 'a']
			s_entropies = [float(t[5]) for t in tweets if t[4] == 's']
			n_entropies = [float(t[5]) for t in tweets if t[4] == 'n']
			u_entropies = [float(t[5]) for t in tweets if t[4] == 'u']
			nu_entropies = np.concatenate((n_entropies, u_entropies), axis=0)
			avg_a = sum(a_entropies) / len(a_entropies)
			avg_s = sum(s_entropies) / len(s_entropies)
			avg_n = sum(n_entropies) / len(n_entropies)
			avg_u = sum(u_entropies) / len(u_entropies)
			avg_nu = sum(nu_entropies) / len(nu_entropies)
			to_write = str(date_mask[i]) + ' ' + str(avg_a) + ' ' + str(avg_s) + ' ' + str(avg_n) + ' ' + str(avg_u) + ' ' + str(avg_nu)
			print(to_write)
			f.write(to_write + '\n')

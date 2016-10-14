from itertools import izip_longest

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

n = 200000

with open('data/full_tweet_data/climate_2015_09_04.txt') as f:
    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
	print("Writing to file climate_small_chunk_" + str(i * n) + ".txt")
        with open('climate_small_chunk_{0}.txt'.format(i * n), 'w') as fout:
            fout.writelines(g)

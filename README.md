# Sentiment analysis on major climate change events

## Direction
The goal of this project is to analyze major climate change events and discuss their effect on the sentiments of active twitter users. 
This is to be done by using natural language processing (NLP) techniques in machine learning.
Two support vector classifiers in succession are used to determine a user's sentiment on climate change.
Based on this classifier, changes in a user's sentiment as well as the 
sentiment of the general population can be analyzed over a period of time.

## Files and Development
* `svm.py` was the first attempt using a single step linear SVC.
* `2stepsvm.py` is the refined version of `svm.py` that incorporates various machine learning techniques such as feature extraction and selection. A 2 step training/evaluation process is used. The first step determines whether or not the tweet contains a sentiment, and the second step determines whether the sentiment is positive or negative. A flag called `PREDICT` determines whether to interpolate results to the dataset for analysis purposes.
* `make_timeseries_data.py`, `fix_timeseries_data.py`, and `make_timeseries_graph.py` are files to generate timeseries graphs as shown in the analysis folder.
* `make_autocorr_graph.py` is a file that uses data generated by the output of `fix_timeseries_data.py` to create a graph showing the autocorrelations by day.
* `make_switcher_data.py` and `make_switcher_graph.py` are files to generate graphs showing statistics of sentiment-switching users as shown in the analysis folder.
* `make_lifetime_data.py` and `make_lifetime_graph.py` are files to generate graphs showing retweet distributions and tweet "lifetime" as shown in the analysis folder.
* `make_total_tweets_data.py` and `make_total_tweets_graph.py` are files to generate graphs showing the total number of tweets per day.
* `util.py` contains various utility functions, some of which are deprecated (that were used to parse and import Vince Talbot's data from last term).
* `import_vince_data.py` is a script that uses several util.py functions to import data from text file format into database format.
* `label_data.py` is a script that allows for easy insertion of labelled data into a database. 
* `word_counter.py` is a script that allows for parsing of tweets per day - the purpose being to analyze distributions of words on a specific day.
* `copy_data_to_text.py` is a script that copies all tweets with sentiments to a text file.
* `create_db_tables.py` generates a database with table names corresponding to files in `get_time_mask()` in util.
* `find_multiple_tweets.sql` is an sql file containing a variety of multipurpose queries in no particular order.
* `merge_sentiment_data.py` is a script that copies all tweets with sentiment into a table called `full_sentiments`.

## Generated / Omitted Files and Directories
* `data/full_tweet_data/climate_20xx_mm_dd.txt` should contain the tweet data files, with tweets of the form: `{"created_at":"Tue Apr 07 10:40:31 +0000 2015":::text: "RT @strebormt: Is anyone else sick of @DoctorKarl Spruiking LNP propaganda re #ChallengeofChange?Still ignoring #climate change and gunning\u2026":::id: 27800134 :::screen name: Peter_Dickerson","location":"Australia":::followers count: 147511,"friends_count":150260:::retweet count: 4}`
* `data/predicted_data.db` is generated by `create_db_tables.py` and filled with data by `2stepsvm.py`.
* `data/full_sentiments.txt` and `data/lifetime_data.txt` are generated by `copy_data_to_text.py` and `make_lifetime_data.py` respectively.

## Credits and Acknowledgements
Thanks to Chris Bauch, Madhur Anand, Vince Talbot, Demetri Pananos, Justin Schonfeld, and Zach Dockstader for their guidance and/or contribution to this project.

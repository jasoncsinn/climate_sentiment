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
* `util.py` contains various utility functions, some of which are deprecated (that were used to parse and import Vince Talbot's data from last term).
* `import_vince_data.py` is a script that uses several util.py functions to import data from text file format into database format.
* `label_data.py` is a script that allows for easy insertion of labelled data into a database. 
* `make_timeseries_data.py`, `fix_timeseries_data.py`, and `make_timeseries_graph.py` are files to generate timeseries graphs as shown in the analysis folder.
* `make_switcher_data.py` and `make_switcher_graph.py` are files to generate graphs showing statistics of sentiment-switching users as shown in the analysis folder.

## Credits and Acknowledgements
Thanks to Chris Bauch, Madhur Anand, Vince Talbot, Demetri Pananos, Justin Schonfeld, and Zach Dockstader for their guidance and contribution to this project.

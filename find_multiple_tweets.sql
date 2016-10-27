/*SELECT *
FROM sentiments
GROUP BY username
HAVING ( COUNT (username) > 1)*/

/*SELECT * FROM full_sentiments WHERE username in
(SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1))
ORDER BY username,date,sentiment*/

--SELECT * FROM full_sentiments ORDER BY username,date
--SELECT date,sentiment FROM full_sentiments WHERE username='0001Angel'

--SELECT COUNT(*) FROM climate_2015_04_14 WHERE not sentiment='n'

--SELECT COUNT(*) FROM tweets
--SELECT * FROM tweets order by date
--SELECT * FROM tweets WHERE username='leafyflower1'

--SELECT * FROM climate_2016_07_29 WHERE sentiment='s'

--SELECT text,username FROM full_sentiments WHERE NOT text LIKE 'RT %'

--SELECT username FROM sentiments GROUP BY username HAVING (COUNT(username) > 1)

--SELECT * FROM full_sentiments WHERE username = 'Col_Connaughton' order by date, sentiment

--SELECT COUNT(*) FROM full_sentiments

--INSERT INTO full_sentiments (text,date,username,location,sentiment)
--SELECT text,date,username,location,sentiment FROM climate_2016_04_29 WHERE not sentiment='n'
--SELECT COUNT(*) FROM full_sentiments

SELECT * FROM climate_2016_05_06 WHERE date like '%May 01%' and sentiment='a'
--SELECT * FROM climate_2016_09_30 WHERE date like '%Sep 27%'  and sentiment='s'
--SELECT * FROM tweets WHERE date like '%Jul%'
--SELECT COUNT(*) FROM full_sentiments
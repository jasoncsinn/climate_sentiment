/*SELECT *
FROM sentiments
GROUP BY username
HAVING ( COUNT (username) > 1)*/

/*SELECT * FROM full_sentiments WHERE username in
(SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1))
ORDER BY username,date,sentiment*/

--SELECT * FROM climate_2016_07_29 WHERE sentiment='s'

SELECT text,username FROM full_sentiments WHERE NOT text LIKE 'RT %'

--SELECT username FROM sentiments GROUP BY username HAVING (COUNT(username) > 1)

--SELECT * FROM full_sentiments WHERE username = 'Col_Connaughton' order by date, sentiment

--INSERT INTO full_sentiments (text,date,username,location,sentiment)
--SELECT text,date,username,location,sentiment FROM climate_2016_08_19 WHERE sentiment='s'
--SELECT COUNT(*) FROM full_sentiments
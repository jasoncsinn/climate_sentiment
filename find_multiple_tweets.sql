/*SELECT *
FROM sentiments
GROUP BY username
HAVING ( COUNT (username) > 1)*/

--SELECT * FROM full_sentiments WHERE username in
--(SELECT username FROM full_sentiments GROUP BY username HAVING (COUNT(username) > 1))
--ORDER BY date

SELECT * FROM climate_2016_05_06 WHERE sentiment='a'

--SELECT username FROM sentiments GROUP BY username HAVING (COUNT(username) > 1)

--SELECT * FROM sentiments WHERE username = 'polar_plankton' ORDER BY date

--INSERT INTO full_sentiments (text,date,username,location,sentiment)
--SELECT text,date,username,location,sentiment FROM climate_2016_08_19 WHERE sentiment='s'
--SELECT COUNT(*) FROM full_sentiments
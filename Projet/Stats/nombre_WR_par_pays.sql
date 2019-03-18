SELECT  COUNT(*),countryName
FROM(
SELECT best, country.countryName
FROM result
NATURAL JOIN person
NATURAL JOIN country
WHERE recordSingleType = "WR"
UNION
SELECT average, country.countryName
FROM result
NATURAL JOIN person
NATURAL JOIN country
WHERE recordAverageType = "WR"
) as a 
GROUP BY countryName
ORDER BY COUNT(*) DESC
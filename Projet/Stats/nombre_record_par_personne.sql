SELECT COUNT(*), personName,countryName 
FROM(
SELECT best, person.personName, country.countryName
FROM result
NATURAL JOIN person
NATURAL JOIN country
WHERE recordSingleType NOT IN ("")
UNION
SELECT average, person.personName, country.countryName
FROM result
NATURAL JOIN person
NATURAL JOIN country
WHERE recordAverageType NOT IN ("")
) as a
GROUP BY personName
ORDER BY COUNT(*) DESC
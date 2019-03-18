SELECT average, event.eventName, competition.competitionName, country.countryName, value1, value2, value3, value4, value5
FROM result
NATURAL JOIN country
NATURAL JOIN city
NATURAL JOIN Competition
NATURAL JOIN event
LEFT JOIN person ON person.personId = result.personId
WHERE	recordAverageType NOT IN ("")
	AND person.personName = "Anthony Lafourcade"
ORDER BY average DESC
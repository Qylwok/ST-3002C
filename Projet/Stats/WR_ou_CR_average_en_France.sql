SELECT average, continent.continentName, event.eventName, competition.competitionName, person.personName, value1, value2, value3, value4, value5
FROM result
NATURAL JOIN country
NATURAL JOIN city
NATURAL JOIN Competition
NATURAL JOIN event
LEFT JOIN person ON person.personId = result.personId
LEFT JOIN continent ON continent.recordName = recordAverageType
WHERE	recordAverageType NOT IN ("", "NR")
	AND country.countryName = "France"
ORDER BY event.eventName
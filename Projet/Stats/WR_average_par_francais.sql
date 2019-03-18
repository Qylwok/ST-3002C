SELECT average, event.eventName, competition.competitionName, person.personName, value1, value2, value3, value4, value5
FROM result
NATURAL JOIN person
NATURAL JOIN country
NATURAL JOIN event
LEFT JOIN competition on result.competitionId = competition.competitionId
WHERE	recordAverageType = "WR"
	AND country.countryName = "France"
ORDER BY event.eventName
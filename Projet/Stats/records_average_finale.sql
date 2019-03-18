SELECT average, event.eventName, roundType.roundTypeName, competition.competitionName, person.personName, country.countryName, value1, value2, value3, value4, value5
FROM result
NATURAL JOIN roundtype
NATURAL JOIN person
NATURAL JOIN country
NATURAL JOIN event
LEFT JOIN competition on result.competitionId = competition.competitionId
WHERE	roundType.roundTypeName = "Final"
	OR roundType.roundTypeName = "Combined Final"
	AND	recordAverageType NOT IN ("")
ORDER BY countryName, average DESC
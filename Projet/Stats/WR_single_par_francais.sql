SELECT best, event.eventName, competition.competitionName, person.personName
FROM result
NATURAL JOIN person
NATURAL JOIN country
NATURAL JOIN event
LEFT JOIN competition on result.competitionId = competition.competitionId
WHERE	recordSingleType = "WR"
	AND country.countryName = "France"
ORDER BY event.eventName
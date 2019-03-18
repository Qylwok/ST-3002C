SELECT best, competition.competitionName, person.personName, country.countryName
FROM result
NATURAL JOIN person
NATURAL JOIN country
NATURAL JOIN event
LEFT JOIN competition on result.competitionId = competition.competitionId
WHERE	event.eventName = "3x3x3 Cube"
	AND	recordSingleType NOT IN ("")
ORDER BY countryName, best DESC
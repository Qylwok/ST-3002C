SELECT best, event.eventName, roundType.roundTypeName, competition.competitionName, person.personName, country.countryName
FROM result
NATURAL JOIN roundtype
NATURAL JOIN person
NATURAL JOIN country
NATURAL JOIN event
LEFT JOIN competition on result.competitionId = competition.competitionId
WHERE	roundType.roundTypeName = "Final"
	OR roundType.roundTypeName = "Combined Final"
	AND	recordSingleType NOT IN ("")
ORDER BY countryName, best DESC
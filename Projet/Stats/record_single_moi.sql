SELECT best, event.eventName, competition.competitionName, country.countryName
FROM result
NATURAL JOIN country
NATURAL JOIN city
NATURAL JOIN Competition
NATURAL JOIN event
LEFT JOIN person ON person.personId = result.personId
WHERE	recordSingleType NOT IN ("")
	AND person.personName = "Anthony Lafourcade"
ORDER BY best DESC
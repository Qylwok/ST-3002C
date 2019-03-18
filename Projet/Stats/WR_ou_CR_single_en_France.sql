SELECT best, recordSingleType, event.eventName, competition.competitionName, person.personName
FROM result
NATURAL JOIN country
NATURAL JOIN city
NATURAL JOIN Competition
NATURAL JOIN event
LEFT JOIN person ON person.personId = result.personId
WHERE	recordSingleType NOT IN ("", "NR")
	AND country.countryName = "France"
ORDER BY event.eventName
-- EXERCICE 1 : Requêtes SQL

-- Question 1
    -- Façon 1
SELECT code_ATC4, code_ATC5, libelle_ATC4 , libelle_ATC5 
FROM ATC4 
NATURAL JOIN ATC5;

    -- Façon 2
SELECT ATC4.code_ATC4, code_ATC5, libelle_ATC4 , libelle_ATC5 
FROM ATC5 LEFT JOIN ATC4 ON ATC4.code_ATC4 = ATC5.code_ATC4;

-- Question 2
SELECT * 
FROM ATC5   NATURAL JOIN ATC4
            NATURAL JOIN ATC3
            NATURAL JOIN ATC2
            NATURAL JOIN ATC1;

SELECT * 
FROM ATC5   LEFT JOIN ATC4 ON ATC5.code_ATC4 = ATC4.code_ATC4
            LEFT JOIN ATC3 ON ATC4.code_ATC3 = ATC3.code_ATC3
            LEFT JOIN ATC2 ON ATC3.code_ATC2 = ATC2.code_ATC2
            LEFT JOIN ATC1 ON ATC2.code_ATC1 = ATC1.code_ATC1
;

-- Question 3
SELECT libelle_ATC5, libelle_ATC4, libelle_ATC3, libelle_ATC2, libelle_ATC1 
FROM ATC5   NATURAL JOIN ATC4
            NATURAL JOIN ATC3
            NATURAL JOIN ATC2
            NATURAL JOIN ATC1
WHERE LOWER(libelle_ATC5) = 'amoxicilline'
;

-- Question 4
SELECT libelle_ATC5, libelle_ATC4, libelle_ATC3, libelle_ATC2, libelle_ATC1 
FROM ATC5   NATURAL JOIN ATC4
            NATURAL JOIN ATC3
            NATURAL JOIN ATC2
            NATURAL JOIN ATC1
WHERE LOWER(libelle_ATC5) LIKE '%ine'
;

-- Question 5
SELECT libelle_ATC5, libelle_ATC4, libelle_ATC3, libelle_ATC2, libelle_ATC1 
FROM ATC5   NATURAL JOIN ATC4
            NATURAL JOIN ATC3
            NATURAL JOIN ATC2
            NATURAL JOIN ATC1
WHERE LOWER(libelle_ATC3) NOT LIKE '%qu%'
;

-- Question 6
SELECT RPPS, nom, prenom, specialite 
FROM Medecin 
    LEFT JOIN Personnel_hospitalier ON Medecin.RPPS = Personnel_hospitalier.id_personnel
;

-- Question 7
SELECT RPPS, nom, prenom, specialite 
FROM Medecin 
    LEFT JOIN Personnel_hospitalier ON Medecin.RPPS = Personnel_hospitalier.id_personnel
GROUP BY specialite
;

-- Question 8
SELECT RPPS, nom, prenom, specialite 
FROM Medecin 
    LEFT JOIN Personnel_hospitalier ON Medecin.RPPS = Personnel_hospitalier.id_personnel
GROUP BY specialite DESC
;

-- Question 9
SELECT DISTINCT nom, prenom 
FROM Prescription 
    NATURAL JOIN Medecin
    LEFT JOIN Personnel_hospitalier ON Medecin.RPPS = Personnel_hospitalier.id_personnel
;

-- Question 10
SELECT DISTINCT Personnel_hospitalier.nom, Personnel_hospitalier.prenom 
FROM Prescription 
    NATURAL JOIN Medecin
    LEFT JOIN Personnel_hospitalier ON Medecin.RPPS = Personnel_hospitalier.id_personnel
    LEFT JOIN Patient ON Patient.IPP = Prescription.IPP
WHERE Patient.IPP = 800613
;

-- Question 11
SELECT DISTINCT Patient.nom, Patient.prenom, Patient.sexe
FROM Patient 
    NATURAL JOIN Administration
    LEFT JOIN Infirmier ON Administration.id_infirmier = Infirmier.ADELI
WHERE Infirmier.ADELI = 314
;

-- Question 12
SELECT *
FROM Prescription 
WHERE CURRENT_TIMESTAMP() < date_heure_prescription
;

-- Question 13
SELECT *
FROM Prescription 
    NATURAL JOIN Medicament
WHERE LOWER(Medicament.DCI) = 'levofloxacine'
;

-- Question 14
SELECT Administration.id_infirmier, Administration.IPP, Administration.cip, Administration.date_heure_administration
FROM Administration 
    NATURAL JOIN Medicament
WHERE LOWER(Medicament.DCI) = 'ceftriaxone'
;

-- Question 15
SELECT Prescription.*
FROM Prescription 
    NATURAL JOIN Patient
WHERE YEAR(Patient.date_naissance) = 1967
;

-- Question 16
SELECT Medicament.*
FROM Medicament 
    NATURAL JOIN Administration
    NATURAL JOIN Patient
WHERE YEAR(Patient.date_naissance) BETWEEN 1960 AND 1970
;

-- Question 17
SELECT Medicament.*
FROM Medicament 
    NATURAL JOIN Administration
    NATURAL JOIN Patient
WHERE YEAR(Patient.date_naissance) % 2 = 0
;

-- Question 18
-- LMAO SKIPPED

-- Question 19
-- LMAO RESKIPPED

-- Question 20
-- Ne marche pas
SELECT id_personnel, nom, prenom
FROM Personnel_hospitalier

EXCEPT

SELECT id_personnel, nom, prenom
FROM Personnel_hospitalier
LEFT JOIN Pharmacien ON Personnel_hospitalier.id_personnel = Pharmacien.RPPS
;
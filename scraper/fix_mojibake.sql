-- Fixar mojibake i Supabase: "SkÃ¥ne" -> "Skåne", "MalmÃ¶" -> "Malmö" osv.
-- Orsak: CSV importerades som Latin-1 men innehöll UTF-8, vilket dubbelkodade
-- alla å/ä/ö. Vi avkodar dem genom att skriva om strängen som Latin-1-bytes
-- och sen läsa tillbaka som UTF-8.

-- 1) Kolla hur manga rader som ar drabbade (forvantat: ~2210)
SELECT COUNT(*) AS mojibake_rader
FROM events
WHERE area LIKE '%Ã%';

-- 2) Forhandsgranska vad som kommer att hanta (topp 20)
SELECT
  area AS fran,
  convert_from(convert_to(area, 'LATIN1'), 'UTF8') AS till,
  COUNT(*) AS antal
FROM events
WHERE area LIKE '%Ã%'
GROUP BY area
ORDER BY antal DESC
LIMIT 20;

-- 3) KÖR den riktiga uppdateringen (tar nagra sekunder)
UPDATE events
SET area = convert_from(convert_to(area, 'LATIN1'), 'UTF8')
WHERE area LIKE '%Ã%';

-- 4) Verifiera att inga mojibake-rader finns kvar
SELECT COUNT(*) AS kvar_mojibake
FROM events
WHERE area LIKE '%Ã%';

-- 5) Topp 15 areor EFTER fix (ska se rena svenska/utlandska namn ut)
SELECT area, COUNT(*) AS antal
FROM events
GROUP BY area
ORDER BY antal DESC
LIMIT 15;

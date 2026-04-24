-- Rensar rader dar AI:n gav ett personnamn eller annat ogiltigt svar
-- istallet for en riktig plats. Dessa hamnar alla pa default-koordinaten
-- (62, 17) mitt i Sverige och bidrar till klumpen.

-- 1) Forhandsgranska vad som kommer att tas bort
SELECT area, COUNT(*) AS antal
FROM events
WHERE area IN (
    'Johans', 'Peter', 'Karl', 'Kristian', 'Hamilton', 'Mansfelds',
    'Renvall', 'Kungliga Krigsvetenskapsakademiens', 'Napoleonkrigen',
    'Kalmarunionen', 'Europa', 'Europas', 'Norden', 'Nordens',
    'Östeuropa', 'Östersjön', 'Utländsk', 'Utländskt',
    'Stockholms', 'Göteborgs', 'Norrköpings', 'Raseborgs',
    'Riksarkivet', 'Sveriges'
)
   OR area IS NULL
   OR area = ''
   OR area = 'Sverige'
   OR area = 'Okänd'
ORDER BY antal DESC;

-- 2) Ta bort dessa skrap-rader
DELETE FROM events
WHERE area IN (
    'Johans', 'Peter', 'Karl', 'Kristian', 'Hamilton', 'Mansfelds',
    'Renvall', 'Kungliga Krigsvetenskapsakademiens', 'Napoleonkrigen',
    'Kalmarunionen', 'Europa', 'Europas', 'Norden', 'Nordens',
    'Östeuropa', 'Utländsk', 'Utländskt',
    'Stockholms', 'Göteborgs', 'Norrköpings', 'Raseborgs',
    'Riksarkivet', 'Sveriges'
)
   OR area IS NULL
   OR area = ''
   OR area = 'Sverige'
   OR area = 'Okänd';

-- 3) Verifiera
SELECT COUNT(*) AS total_kvar FROM events;

import { getCoords } from './coordinates';

function isForeign(area) {
    if (!area) return false;
    const key = String(area).toLowerCase().trim();
    const swedishRegions = new Set([
        'sverige', 'svealand', 'götaland', 'norrland',
        'blekinge', 'bohuslän', 'dalarna', 'dalsland', 'gotland',
        'gästrikland', 'halland', 'hälsingland', 'härjedalen', 'jämtland',
        'lappland', 'medelpad', 'norrbotten', 'närke', 'skåne', 'småland',
        'södermanland', 'uppland', 'värmland', 'västerbotten', 'västergötland',
        'västmanland', 'ångermanland', 'öland', 'östergötland'
    ]);
    if (swedishRegions.has(key)) return false;

    const { lat, lng } = getCoords(area);
    if (lat === 62 && lng === 17) return false;
    return lat < 55 || lat > 69.5 || lng < 10.5 || lng > 24.5;
}

export const CATEGORIES = {
    krigUtomlands: {
        name: 'Krig utomlands',
        color: '#ffb266',
        filter: (event) => isForeign(event.area) && (
            event.title?.toLowerCase().includes('krig') ||
            event.description?.toLowerCase().includes('slag') ||
            event.description?.toLowerCase().includes('strid') ||
            event.description?.toLowerCase().includes('kamp')
        )
    },
    krigOchKonflikt: {
        name: 'Krig och konflikt',
        color: '#7d7dec',
        filter: (event) => event.title?.toLowerCase().includes('krig') ||
                          event.description?.toLowerCase().includes('slag') ||
                          event.description?.toLowerCase().includes('strid') ||
                          event.description?.toLowerCase().includes('kamp')
    },
    uppfinningar: {
        name: 'Uppfinningar',
        color: '#8eff8e',
        filter: (event) => event.title?.toLowerCase().includes('uppfin') ||
                          event.description?.toLowerCase().includes('uppfin')
    },
    innanKristus: {
        name: 'Innan Kristus',
        color: '#ff8b8b',
        filter: (event) => event.year < 0
    }
};

export function getEventCategory(event) {
    for (const [key, category] of Object.entries(CATEGORIES)) {
        if (category.filter(event)) {
            return { key, ...category };
        }
    }
    return { key: 'other', name: 'Övrigt', color: '#888888' };
}

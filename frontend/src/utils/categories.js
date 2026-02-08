export const CATEGORIES = {
    krigOchKonflikt: {
        name: 'Krig och konflikt',
        color: '#4444ff',
        filter: (event) => event.title?.toLowerCase().includes('krig') || 
                          event.description?.toLowerCase().includes('slag') ||
                          event.description?.toLowerCase().includes('strid') ||
                          event.description?.toLowerCase().includes('kamp')
    },
    uppfinningar: {
        name: 'Uppfinningar',
        color: '#44ff44',
        filter: (event) => event.title?.toLowerCase().includes('uppfin') ||
                          event.description?.toLowerCase().includes('uppfin')
    },
    innanKristus: {
        name: 'Innan Kristus',
        color: '#ff4444',
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
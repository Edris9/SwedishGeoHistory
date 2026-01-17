const API_URL = 'http://localhost:5007/api';

export async function getEvents(from, to) {
    let url = `${API_URL}/events`;
    
    if (from && to) {
        url += `?from=${from}&to=${to}`;
    }
    
    const response = await fetch(url);
    return response.json();
}

export async function getEventById(id) {
    const response = await fetch(`${API_URL}/events/${id}`);
    return response.json();
}
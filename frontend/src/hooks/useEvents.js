import { useState, useEffect } from 'react';
import { getEvents } from '../services/api';

export function useEvents() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function loadEvents() {
            try {
                const data = await getEvents();
                setEvents(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        loadEvents();
    }, []);

    return { events, loading, error };
}
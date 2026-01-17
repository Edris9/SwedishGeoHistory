import { useEffect, useState } from 'react';
import MapView from './components/Map';
import EventPopup from './components/EventPopup';
import { getEvents } from './services/api';

export default function App() {
    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);

    useEffect(() => {
        async function loadEvents() {
            const data = await getEvents();
            setEvents(data);
        }
        loadEvents();
    }, []);

    return (
        <div>
            <MapView 
                events={events} 
                onEventClick={(event) => setSelectedEvent(event)} 
            />
            
            {selectedEvent && (
                <EventPopup 
                    event={selectedEvent} 
                    onClose={() => setSelectedEvent(null)} 
                />
            )}
        </div>
    );
}
import { useEffect, useState } from 'react';
import MapView from './components/Map';
import EventPopup from './components/EventPopup';
import Timeline from './components/Timeline';
import { getEvents } from './services/api';

export default function App() {
    const [events, setEvents] = useState([]);
    const [filteredEvents, setFilteredEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [selectedYear, setSelectedYear] = useState(2026);

    useEffect(() => {
        async function loadEvents() {
            const data = await getEvents();
            setEvents(data);
            setFilteredEvents(data);
        }
        loadEvents();
    }, []);

    const handleYearChange = (year) => {
        setSelectedYear(year);
        const filtered = events.filter(e => e.year <= year);
        setFilteredEvents(filtered);
    };

    return (
        <div>
            <MapView 
                events={filteredEvents} 
                onEventClick={(event) => setSelectedEvent(event)} 
            />
            
            <Timeline 
                minYear={-12000}
                maxYear={2026}  // <-- Är detta 2026 eller 0?
                onYearChange={handleYearChange}
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
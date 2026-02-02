import { useEffect, useState } from 'react';
import MapView from './components/Map';
import EventPopup from './components/EventPopup';
import Timeline from './components/Timeline';
import SettingsMenu from './components/SettingsMenu';
import { getEvents } from './services/api';

export default function App() {
    const [events, setEvents] = useState([]);
    const [filteredEvents, setFilteredEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [selectedYear, setSelectedYear] = useState(2026);
    const [showAll, setShowAll] = useState(false);

    useEffect(() => {
        async function loadEvents() {
            const data = await getEvents();
            setEvents(data);
            setFilteredEvents(data);
        }
        loadEvents();
    }, []);

    useEffect(() => {
        if (showAll) {
            setFilteredEvents(events);
        } else {
            const filtered = events.filter(e => e.year <= selectedYear);
            setFilteredEvents(filtered);
        }
    }, [showAll, selectedYear, events]);

    const handleYearChange = (year) => {
        setSelectedYear(year);
    };

    return (
        <div>
            <MapView 
                events={filteredEvents} 
                onEventClick={(event) => setSelectedEvent(event)} 
            />
            
            <SettingsMenu showAll={showAll} setShowAll={setShowAll} />
            
            {!showAll && (
                <Timeline 
                    minYear={-12000}
                    maxYear={2026}
                    onYearChange={handleYearChange}
                />
            )}
            
            {selectedEvent && (
                <EventPopup 
                    event={selectedEvent} 
                    onClose={() => setSelectedEvent(null)} 
                />
            )}
        </div>
    );
}
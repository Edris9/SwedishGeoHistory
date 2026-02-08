// App.jsx
import { useEffect, useState } from 'react';
import MapView from './components/Map';
import EventPopup from './components/EventPopup';
import Timeline from './components/Timeline';
import SettingsMenu from './components/SettingsMenu';
import Startsida from './components/Startsida';   
import { getEvents } from './services/api';
import ProjectStatusPopup from './components/ProjectStatusPopup';   

export default function App() {
    const [events, setEvents] = useState([]);
    const [filteredEvents, setFilteredEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [selectedYear, setSelectedYear] = useState(2026);
    const [showAll, setShowAll] = useState(false);
    const [showStartscreen, setShowStartscreen] = useState(true);
    
    // ← Lägg till denna rad (detta saknades troligen)
    const [showStatus, setShowStatus] = useState(true);

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

    const handleStartExploring = () => {
        setShowStartscreen(false);
    };

    return (
        <>
            {/* Projektstatus visas alltid först – stäng för att se resten */}
            {showStatus && (
                <ProjectStatusPopup onClose={() => setShowStatus(false)} />
            )}

            {showStartscreen ? (
                <Startsida onStart={handleStartExploring} />
            ) : (
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
            )}
        </>
    );
}
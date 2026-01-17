import { useState } from 'react';
import './Timeline.css';

export default function Timeline({ minYear, maxYear, onYearChange }) {
    const [selectedYear, setSelectedYear] = useState(maxYear);

    const handleChange = (e) => {
        const year = parseInt(e.target.value);
        setSelectedYear(year);
        onYearChange(year);
    };

    const formatYear = (year) => {
        if (year < 0) return `${Math.abs(year)} f.Kr`;
        return `${year} e.Kr`;
    };

    return (
        <div className="timeline-container">
            <div className="timeline-year">{formatYear(selectedYear)}</div>
            <input
                type="range"
                min={minYear}
                max={maxYear}
                value={selectedYear}
                onChange={handleChange}
                className="timeline-slider"
            />
            <div className="timeline-labels">
                <span>{formatYear(minYear)}</span>
                <span>{formatYear(maxYear)}</span>
            </div>
        </div>
    );
}
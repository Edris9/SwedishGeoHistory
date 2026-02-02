import React, { useState, useRef, useEffect } from 'react';
import './Timeline.css';

export default function Timeline({ minYear = -12000, maxYear = 2026, onYearChange }) {
    const [selectedYear, setSelectedYear] = useState(maxYear);
    const containerRef = useRef(null);
    const isDragging = useRef(false);
    const startX = useRef(0);
    const startYear = useRef(0);

    const updateYear = (year) => {
        const clampedYear = Math.max(minYear, Math.min(maxYear, year));
        setSelectedYear(clampedYear);
        if (onYearChange) onYearChange(clampedYear);
    };

    const handleChange = (e) => {
        updateYear(parseInt(e.target.value));
    };

    // Scroll med mushjul
    const handleWheel = (e) => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? 25 : -25;
        updateYear(selectedYear + delta);
    };

    // Touch & Mouse drag
    const handleStart = (clientX) => {
        isDragging.current = true;
        startX.current = clientX;
        startYear.current = selectedYear;
    };

    const handleMove = (clientX) => {
        if (!isDragging.current || !containerRef.current) return;
        
        const containerWidth = containerRef.current.offsetWidth;
        const deltaX = clientX - startX.current;
        const yearRange = maxYear - minYear;
        const yearDelta = -(deltaX / containerWidth) * yearRange * 0.5;
        
        updateYear(Math.round(startYear.current + yearDelta));
    };

    const handleEnd = () => {
        isDragging.current = false;
    };

    // Mouse events
    const handleMouseDown = (e) => handleStart(e.clientX);
    const handleMouseMove = (e) => handleMove(e.clientX);
    const handleMouseUp = () => handleEnd();

    // Touch events
    const handleTouchStart = (e) => handleStart(e.touches[0].clientX);
    const handleTouchMove = (e) => handleMove(e.touches[0].clientX);
    const handleTouchEnd = () => handleEnd();

    useEffect(() => {
        const container = containerRef.current;
        if (!container) return;

        container.addEventListener('wheel', handleWheel, { passive: false });
        
        return () => {
            container.removeEventListener('wheel', handleWheel);
        };
    }, [selectedYear]);

    

    const formatYear = (year) => {
        if (year < 0) return `${Math.abs(year)} f.Kr`;
        if (year === 0) return '0';
        return `${year} e.Kr`;
    };

    // Skapa streck - 100 stycken
    const tickCount = 250;
    const ticks = Array.from({ length: tickCount }, (_, i) => i);

    return (
        <div 
            className="timeline"
            ref={containerRef}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
        >
            <div className="timeline-bg"></div>
            
            <div className="timeline-content">
                <div className="timeline-year">{formatYear(selectedYear)}</div>
                
                <svg className="timeline-svg" viewBox="0 0 1000 120" preserveAspectRatio="none">
                    {ticks.map((_, i) => {
                        // Position från 0 till 1
                        const t = i / (tickCount - 1);
                        
                        // X position
                        const x = 50 + t * 900;
                        
                        // Y följer en båge (sinus-kurva för mjuk båge)
                        const curveDepth = 50;
                        const y = curveDepth * (1 - Math.sin(t * Math.PI));
                        
                        // Vinkel - tangent till kurvan
                        const angle = Math.cos(t * Math.PI) * 40;
                        
                        // Är detta strecket aktivt?
                        const progress = (selectedYear - minYear) / (maxYear - minYear);
                        const isActive = Math.abs(t - progress) < 0.002;
                        
                        const height = isActive ? 35 : 20;
                        const strokeWidth = isActive ? 3 : 1.5;
                        const color = isActive ? '#3b82f6' : '#333';

                        return (
                            <line
                                key={i}
                                x1={x}
                                y1={y + 70}
                                x2={x + Math.sin(angle * Math.PI / 180) * height}
                                y2={y + 70 - Math.cos(angle * Math.PI / 180) * height}
                                stroke={color}
                                strokeWidth={strokeWidth}
                                strokeLinecap="round"
                            />
                        );
                    })}
                </svg>

                <input
                    type="range"
                    min={minYear}
                    max={maxYear}
                    value={selectedYear}
                    onChange={handleChange}
                    className="timeline-slider"
                />
            </div>
        </div>
    );
}
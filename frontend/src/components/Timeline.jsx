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
    onYearChange?.(clampedYear);
  };

  const handleChange = (e) => {
    updateYear(parseInt(e.target.value, 10));
  };

  // Scroll med mushjul
  const handleWheel = (e) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 30 : -30;
    updateYear(selectedYear + delta);
  };

  // Drag / touch start
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
    const yearDelta = -(deltaX / containerWidth) * yearRange * 0.6; // lite känsligare
    updateYear(Math.round(startYear.current + yearDelta));
  };

  const handleEnd = () => {
    isDragging.current = false;
  };

  // Event listeners
  const handleMouseDown = (e) => handleStart(e.clientX);
  const handleMouseMove = (e) => handleMove(e.clientX);
  const handleMouseUp = () => handleEnd();

  const handleTouchStart = (e) => handleStart(e.touches[0].clientX);
  const handleTouchMove = (e) => handleMove(e.touches[0].clientX);
  const handleTouchEnd = () => handleEnd();

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    container.addEventListener('wheel', handleWheel, { passive: false });
    return () => container.removeEventListener('wheel', handleWheel);
  }, [selectedYear]);

  const formatYear = (year) => {
    if (year < 0) return `${Math.abs(year)} f.Kr`;
    if (year === 0) return 'År 0';
    return `${year} e.Kr`;
  };

  // Fler ticks för mjukare känsla (men fortfarande prestandavänligt)
  const tickCount = 320;
  const ticks = Array.from({ length: tickCount }, (_, i) => i);

  const progress = (selectedYear - minYear) / (maxYear - minYear);

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
      onTouchCancel={handleTouchEnd}
    >
      <div className="timeline-bg" />

      <div className="timeline-content">
        <div className="timeline-year-display">
          {formatYear(selectedYear)}
        </div>

        <svg className="timeline-svg" viewBox="0 0 1000 140" preserveAspectRatio="none">
          {ticks.map((_, i) => {
            const t = i / (tickCount - 1);
            const x = 40 + t * 920;

            // Mjuk sinus-kurva
            const curve = 38 * (1 - Math.sin(t * Math.PI));
            const yBase = 90;

            // Aktiv punkt?
            const dist = Math.abs(t - progress);
            const isActive = dist < 0.003;

            const height = isActive ? 48 : 22;
            const strokeWidth = isActive ? 4.2 : 1.8;
            const opacity = isActive ? 1 : Math.max(0.18, 1 - dist * 12);

            // Liten vinkel för 3D-känsla
            const angle = Math.cos(t * Math.PI) * 35;

            return (
              <line
                key={i}
                x1={x}
                y1={yBase + curve}
                x2={x + Math.sin(angle * Math.PI / 180) * height}
                y2={yBase + curve - Math.cos(angle * Math.PI / 180) * height}
                stroke={isActive ? '#ca5b00' : '#ffffff'}
                strokeWidth={strokeWidth}
                strokeOpacity={opacity}
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
          aria-label="Tidslinje år"
        />
      </div>
    </div>
  );
}
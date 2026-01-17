import { useEffect, useRef } from 'react';
import * as maptilersdk from '@maptiler/sdk';
import '@maptiler/sdk/dist/maptiler-sdk.css';

const SWEDEN_COORDS = {
    'halland': { lat: 56.89, lng: 12.80 },
    'bohuslän': { lat: 58.32, lng: 11.45 },
    'skåne': { lat: 55.99, lng: 13.59 },
    'stockholm': { lat: 59.33, lng: 18.07 },
    'göteborg': { lat: 57.71, lng: 11.97 },
    'malmö': { lat: 55.60, lng: 13.00 },
    'uppsala': { lat: 59.86, lng: 17.64 },
    'dalarna': { lat: 61.09, lng: 14.66 },
    'norrland': { lat: 65.58, lng: 19.50 },
    'gotland': { lat: 57.47, lng: 18.49 },
    'småland': { lat: 57.19, lng: 15.21 },
    'värmland': { lat: 59.73, lng: 13.23 },
    'västergötland': { lat: 58.25, lng: 13.05 },
    'östergötland': { lat: 58.41, lng: 15.62 },
    'södermanland': { lat: 59.03, lng: 16.75 },
    'närke': { lat: 59.10, lng: 15.00 },
    'västmanland': { lat: 59.62, lng: 16.55 },
    'uppland': { lat: 60.00, lng: 17.65 },
    'gästrikland': { lat: 60.67, lng: 17.00 },
    'hälsingland': { lat: 61.73, lng: 16.22 },
    'medelpad': { lat: 62.39, lng: 17.31 },
    'ångermanland': { lat: 63.28, lng: 17.99 },
    'jämtland': { lat: 63.17, lng: 14.64 },
    'västerbotten': { lat: 64.75, lng: 17.00 },
    'norrbotten': { lat: 66.83, lng: 20.20 },
    'lappland': { lat: 67.50, lng: 18.00 },
    'blekinge': { lat: 56.17, lng: 15.58 },
    'öland': { lat: 56.66, lng: 16.64 },
    'dalsland': { lat: 58.88, lng: 12.17 }
};

function getCoords(area) {
    if (!area) return { lat: 62, lng: 17 };
    const key = area.toLowerCase();
    return SWEDEN_COORDS[key] || { lat: 62, lng: 17 };
}

export default function MapView({ events, onEventClick }) {
    const mapContainer = useRef(null);

    useEffect(() => {
        maptilersdk.config.apiKey = 'kNPyqqEDajTwuaZTofx9';

        const map = new maptilersdk.Map({
            container: mapContainer.current,
            style: maptilersdk.MapStyle.HYBRID,
            center: [16, 62],
            zoom: 3,
            projection: 'globe'
        });

        map.on('load', () => {
            events.forEach(event => {
                const coords = getCoords(event.area);

                const marker = document.createElement('div');
                marker.style.width = '15px';
                marker.style.height = '15px';
                marker.style.backgroundColor = '#ff4444';
                marker.style.borderRadius = '50%';
                marker.style.cursor = 'pointer';
                marker.style.border = '2px solid white';

                marker.addEventListener('click', () => onEventClick(event));

                new maptilersdk.Marker({ element: marker })
                    .setLngLat([coords.lng, coords.lat])
                    .addTo(map);
            });
        });

        return () => map.remove();
    }, [events]);

    return <div ref={mapContainer} style={{ width: '100%', height: '100vh' }} />;
}
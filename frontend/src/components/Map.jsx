import { useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import * as maptilersdk from '@maptiler/sdk';
import '@maptiler/sdk/dist/maptiler-sdk.css';
import { SWEDEN_COORDS } from '../utils/coordinates';
import { getEventCategory } from '../utils/categories';

const MapView = forwardRef(({ events, onEventClick }, ref) => {
    const mapContainer = useRef(null);
    const mapInstance = useRef(null);
    const isRotating = useRef(true);
    const markersRef = useRef([]);
    

    useImperativeHandle(ref, () => ({
        flyToSweden: () => {
            if (mapInstance.current) {
                isRotating.current = false;
                mapInstance.current.flyTo({
                    center: [16, 62],
                    zoom: 15,
                    bearing: 0,
                    pitch: 0,
                    duration: 3000
                });
            }
        }
    }));

    useEffect(() => {
        maptilersdk.config.apiKey = 'kNPyqqEDajTwuaZTofx9';

        const map = new maptilersdk.Map({
            container: mapContainer.current,
            style: maptilersdk.MapStyle.HYBRID,
            center: [22, 20],
            zoom: 6.2,                    // starta väldigt utzoomat
            projection: 'globe',
            bearing: 10,
            pitch: 20
        });

        mapInstance.current = map;

        map.on('load', () => {
            let currentZoom = map.getZoom();
            const targetZoom = 3.8;       // mellanzoom under rotation
            const zoomDuration = 8000;    // total tid för zoom + rotation ≈ 8 sek
            const zoomStartTime = Date.now();

            function animate() {
                if (!isRotating.current) return;

                const now = Date.now();
                const progress = Math.min((now - zoomStartTime) / zoomDuration, 1);

                // Gradvis zoom in under rotation
                const newZoom = 1.2 + (targetZoom - 1.9) * progress;
                map.setZoom(newZoom);

                // Rotation
                const center = map.getCenter();
                center.lng += 0.38;           // lite snabbare än tidigare
                map.setCenter(center);

                requestAnimationFrame(animate);
            }

            // Starta animationen
            animate();

            // Efter zoom + rotation → stanna och flytta exakt till Sverige
            setTimeout(() => {
                isRotating.current = false;

                // Förbered globen på rätt sida
                map.jumpTo({               // jumpTo = omedelbar, ingen animation
                    center: [16 + 360, 62], // +360° = samma fysiska plats, men rotation ändras
                    zoom: 3.5,
                    bearing: 0
                });

                // Vänta en frame så det hinner uppdateras
                setTimeout(() => {
                    map.flyTo({
                        center: [16, 62],   // nu tillbaka till normal longitude
                        zoom: 5,
                        bearing: 0,
                        pitch: 25,
                        duration: 3400,
                        essential: true,
                    });
                }, 50);  // väldigt kort delay
            }, 8500); // lite längre än zoom-tiden så det känns naturligt

        });

        // Cleanup
        return () => {
            if (mapInstance.current) {
                mapInstance.current.remove();
            }
        };
    }, []);

    // Markers (oförändrad)
    useEffect(() => {
        if (!mapInstance.current) return;

        markersRef.current.forEach(marker => marker.remove());
        markersRef.current = [];

        events.forEach((event, index) => {
            const coords = getCoords(event.area, index);
            const category = getEventCategory(event);

            const markerEl = document.createElement('div');
            markerEl.style.width = '15px';
            markerEl.style.height = '15px';
            markerEl.style.backgroundColor = category.color;
            markerEl.style.borderRadius = '50%';
            markerEl.style.cursor = 'pointer';
            markerEl.style.border = '2px solid white';
            markerEl.style.boxShadow = '0 2px 5px rgba(0,0,0,0.3)';
            markerEl.style.boxShadow = '0 2px 5px rgba(0,0,0,0.3)';
            markerEl.style.pointerEvents = 'auto';
            markerEl.style.zIndex = '1000';

            markerEl.addEventListener('click', () => onEventClick(event));

            const marker = new maptilersdk.Marker({ element: markerEl })
                .setLngLat([coords.lng, coords.lat])
                .addTo(mapInstance.current);

        markersRef.current.push(marker);
    });
    
}, [events, onEventClick]);

    function getCoords(area, index) {
        const key = area ? area.toLowerCase() : 'sverige';
        const base = SWEDEN_COORDS[key] || { lat: 62, lng: 15 };
        
        const spread = 0.3;
        const offsetLat = (Math.sin(index * 2.5) * spread);
        const offsetLng = (Math.cos(index * 3.7) * spread);
        
        return {
            lat: base.lat + offsetLat,
            lng: base.lng + offsetLng
        };
    }

    return <div ref={mapContainer} style={{ width: '100%', height: '100vh' }} />;
});

export default MapView;
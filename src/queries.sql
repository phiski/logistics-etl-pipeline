-- 1. Überblick: Sendungsvolumen, Gesamtgewicht und durchschnittliche Laufzeit pro Lager
SELECT 
    warehouse AS Lagerstandort,
    COUNT(shipment_id) AS Anzahl_Sendungen,
    ROUND(SUM(weight_kg), 2) AS Gesamtgewicht_kg,
    ROUND(AVG(transit_hours), 1) AS Durchschn_Laufzeit_Std
FROM shipments
GROUP BY warehouse
ORDER BY Anzahl_Sendungen DESC;

-- 2. Qualitäts-Check: Verspätungsquote (> 48 Stunden) nach Lagerstandort
SELECT 
    warehouse AS Lagerstandort,
    COUNT(*) AS Gesamt,
    SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) AS Verspaetet,
    ROUND(100.0 * SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS Verspaetungsquote_Prozent
FROM shipments
GROUP BY warehouse
ORDER BY Verspaetungsquote_Prozent DESC;

-- 3. Zielländer-Analyse: Sendungsverteilung und Durchschnittsgewicht pro Land
SELECT 
    destination_country AS Zielland,
    COUNT(*) AS Anzahl_Sendungen,
    ROUND(AVG(weight_kg), 2) AS Durchschn_Gewicht_kg
FROM shipments
GROUP BY destination_country
ORDER BY Anzahl_Sendungen DESC;

-- 4. Ausreißer-Suche: Die 10 Sendungen mit der längsten Transportdauer
SELECT 
    shipment_id,
    warehouse,
    destination_country,
    ROUND(transit_hours, 1) AS Laufzeit_Std,
    status
FROM shipments
ORDER BY transit_hours DESC
LIMIT 10;
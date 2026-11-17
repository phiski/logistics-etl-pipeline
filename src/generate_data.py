import csv #Tabellen in Textdateien schreiben
import random #Erzeugen von Zufallszahlen und zufällgen Auswahlen
from datetime import datetime, timedelta #datetime und timedelta für Zeitberechnungen
from pathlib import Path #Für den Umgang mit Dateipfaden

def generate_raw_shipments(output_path: str, num_records: int = 500) -> None: #Es werden standartmäßig 500 Datensätze erzeugt
    Path(output_path).parent.mkdir(parents=True, exist_ok=True) #Existiert der Ordner nicht, wird er erstellt

    # Zufallsdaten für die Rohdatensätze erzeugen
    warehouses = ["Dortmund", "Holzwickede", "Hamm", "Unna", "dortmund", "HOLZWICKEDE"]
    countries = ["DE", "Deutschland", "GER", "NL", "Niederlande", "BE", "Belgien"]
    statuses = ["Delivered", "Delayed", "In Transit"]
    
    base_date = datetime(2026, 11, 1)
    records = []

    for i in range(1, num_records + 1): # Die Schleife erzeugt die Rohdatensätze (500 Datensätze)
        shipment_id = f"SHP-{10000 + i}" #f-String für die eindeutige ID der Sendung
        warehouse = random.choice(warehouses) #Zufällige Auswahl eines Lagers aus der Liste
        country = random.choice(countries) #Zufällige Auswahl eines Ziellandes aus der Liste
        
        # Realistische Fehler einbauen: ca. 8% fehlende Gewichte oder negative Werte
        if random.random() < 0.08:
            weight_kg = ""
        elif random.random() < 0.03: # Realistische Fehler einbauen: ca. 3% negative Werte
            weight_kg = -round(random.uniform(1.0, 15.0), 2)
        else: # Normalfall: Gewicht zwischen 0,5 und 45 kg
            weight_kg = round(random.uniform(0.5, 45.0), 2)
            
        dispatch_time = base_date + timedelta(hours=random.randint(0, 300)) # Zufällige Versandszeit innerhalb von 300 Stunden nach dem Basisdatum
        transit_hours = random.randint(12, 96) # Zufällige Laufzeit zwischen 12 und 96 Stunden
        delivery_time = dispatch_time + timedelta(hours=transit_hours) # Zufällige Lieferzeit basierend auf der Laufzeit
        
        # Status basierend auf Laufzeit setzen (über 48h = Delayed)
        status = "Delayed" if transit_hours > 48 else random.choice(["Delivered", "In Transit"])
        
        records.append([
            shipment_id,
            warehouse,
            country,
            weight_kg,
            dispatch_time.strftime("%Y-%m-%d %H:%M:%S"),
            delivery_time.strftime("%Y-%m-%d %H:%M:%S"),
            status
        ])

    # Ca. 5% absichtliche Dubletten hinzufügen
    duplicates = random.sample(records, k=int(num_records * 0.05))
    records.extend(duplicates)
    random.shuffle(records) # Die Reihenfolge der Datensätze wird gemischt, um die Dubletten zufällig zu verteilen

    with open(output_path, mode="w", newline="", encoding="utf-8") as file: # Die Rohdatensätze werden in eine CSV-Datei geschrieben
        writer = csv.writer(file, delimiter=";") # Die CSV-Datei wird mit Semikolon als Trennzeichen erstellt
        writer.writerow([ # Die Kopfzeile der CSV-Datei wird geschrieben
            "shipment_id", "warehouse", "destination_country", 
            "weight_kg", "dispatch_time", "delivery_time", "status"
        ])
        writer.writerows(records) # Die Rohdatensätze werden in die CSV-Datei geschrieben

    print(f"Erfolgreich {len(records)} Rohdatensätze (inkl. Fehler & Dubletten) in '{output_path}' erzeugt.")

if __name__ == "__main__": # Wenn das Skript direkt ausgeführt wird, wird die Funktion aufgerufen, um die Rohdatensätze zu erzeugen
    generate_raw_shipments("data/raw/shipments_raw.csv")
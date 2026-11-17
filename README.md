# Logistics ETL & Data Cleansing Pipeline

Eine automatisierte Datenpipeline in Python und SQL zur Bereinigung, Aufbereitung und Analyse von Logistik- und Sendungsdaten.

## 🎯 Projektziel & Hintergrund
In der Logistik stammen Sendungs- und Lagerdaten häufig aus unterschiedlichen Systemen und enthalten typische Qualitätsmängel wie doppelte Einträge, fehlende Gewichtsangaben oder uneinheitliche Länder- und Standortbezeichnungen. 

Dieses Projekt bildet einen vollständigen **ETL-Prozess (Extract, Transform, Load)** ab, der unsaubere Rohdaten bereinigt, logistische Kennzahlen berechnet und die Daten für SQL-Analysen in einer relationalen Datenbank bereitstellt.

## ⚙️ Funktionen der Pipeline
* **Datengenerierung (`src/generate_data.py`):** Erzeugt simulierte Sendungsdaten inklusive realistischer Datenfehler (Dubletten, negative/fehlende Gewichte, abweichende Schreibweisen).
* **Extract & Transform (`src/pipeline.py`):**
  * Entfernt doppelte Sendungs-IDs.
  * Vereinheitlicht Lagernamen und übersetzt Länderbezeichnungen in ISO-Codes (`DE`, `NL`, `BE`).
  * Bereinigt ungültige Gewichtsangaben mittels Median-Imputation.
  * Berechnet die exakte Transportdauer in Stunden (`transit_hours`) sowie eine Verspätungs-Kennzeichnung (`is_delayed` bei > 48 Std.).
* **Load:** Speichert die bereinigten Daten sowohl als CSV als auch in einer strukturierten **SQLite-Datenbank** (`data/processed/logistics.db`).
* **SQL-Analytics (`src/queries.sql`):** Enthält fertige SQL-Abfragen zur Auswertung von Sendungsvolumen, Gesamtgewicht und Verspätungsquoten pro Lagerstandort.
* **Qualitätssicherung (`tests/test_pipeline.py`):** Automatisierte Unit Tests mit `pytest` zur Absicherung der Datenbereinigungs-Logik.

## 🚀 Installation & Ausführung

1. **Repository klonen & virtuelle Umgebung einrichten:**
   ```bash
   git clone https://github.com
   cd logistics-etl-pipeline
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Rohdaten erzeugen & ETL-Pipeline starten:**
   ```bash
   python src/generate_data.py
   python src/pipeline.py
   ```

4. **Unit Tests ausführen:**
   ```bash
   python -m pytest
   ```
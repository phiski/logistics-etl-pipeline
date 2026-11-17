import sqlite3 # SQLite3 für die Datenbankoperationen
from pathlib import Path
import pandas as pd # Pandas für die Datenmanipulation und -analyse


def extract_data(input_path: str) -> pd.DataFrame:
    """Liest die unsauberen Logistik-Rohdaten aus der CSV-Datei ein."""
    print(f"1. EXTRACT: Lese Rohdaten aus '{input_path}'...")
    df = pd.read_csv(input_path, delimiter=";") # Die Rohdaten werden aus der CSV-Datei eingelesen, wobei das Semikolon als Trennzeichen verwendet wird
    print(f"   -> {len(df)} Zeilen eingelesen.")
    return df

# Data Cleansing und Aufbereitung der Daten
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Bereinigt Datenfehler, vereinheitlicht Formate und berechnet Kennzahlen."""
    print("2. TRANSFORM: Starte Data Cleansing und Aufbereitung...")
    initial_count = len(df)

    # 1. Dubletten anhand der Sendungsnummer entfernen
    df = df.drop_duplicates(subset=["shipment_id"], keep="first").copy()
    print(f"   -> {initial_count - len(df)} doppelte Sendungen entfernt.")

    # 2. Lagernamen vereinheitlichen (z. B. 'dortmund' und 'HOLZWICKEDE' -> 'Dortmund', 'Holzwickede')
    df["warehouse"] = df["warehouse"].str.strip().str.title() # Die Lagernamen werden bereinigt, indem führende und nachfolgende Leerzeichen entfernt und die erste Buchstaben jedes Wortes großgeschrieben werden

    # 3. Ländercodes auf ISO-Standard vereinheitlichen
    country_mapping = {
        "Deutschland": "DE",
        "GER": "DE",
        "DE": "DE",
        "Niederlande": "NL",
        "NL": "NL",
        "Belgien": "BE",
        "BE": "BE",
    }
    df["destination_country"] = df["destination_country"].map(country_mapping).fillna("UNKNOWN") # Die Zielländer werden auf ISO-Standardcodes abgebildet, wobei unbekannte Länder als "UNKNOWN" markiert werden

    # 4. Ungültige Gewichte (leer oder <= 0) bereinigen und durch den Median ersetzen
    df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce") # Die Gewichtsangaben werden in numerische Werte umgewandelt, wobei ungültige Einträge als NaN behandelt werden
    invalid_weights = df["weight_kg"].isna() | (df["weight_kg"] <= 0) # Ungültige Gewichtsangaben werden identifiziert, entweder weil sie leer sind oder einen Wert kleiner oder gleich null haben
    median_weight = df.loc[~invalid_weights, "weight_kg"].median() # Der Median der gültigen Gewichtsangaben wird berechnet, um die ungültigen Werte zu ersetzen
    df.loc[invalid_weights, "weight_kg"] = round(median_weight, 2) # Die ungültigen Gewichtsangaben werden durch den berechneten Median ersetzt, wobei auf zwei Dezimalstellen gerundet wird
    print(f"   -> {invalid_weights.sum()} ungültige Gewichtsangaben durch Median ({median_weight:.2f} kg) ersetzt.")

    # 5. Zeitstempel umwandeln und neue Kennzahl (Transportdauer in Stunden) berechnen
    df["dispatch_time"] = pd.to_datetime(df["dispatch_time"])
    df["delivery_time"] = pd.to_datetime(df["delivery_time"])
    df["transit_hours"] = (df["delivery_time"] - df["dispatch_time"]).dt.total_seconds() / 3600

    # 6. Zusätzliche Qualitäts-Flag für verspätete Lieferungen (> 48 Stunden)
    df["is_delayed"] = df["transit_hours"] > 48

    print(f"   -> Bereinigung abgeschlossen. {len(df)} saubere Datensätze bereit.")
    return df

# Daten in CSV und SQLite-Datenbank speichern
def load_data(df: pd.DataFrame, db_path: str, csv_output_path: str) -> None:
    print(f"3. LOAD: Speichere Ergebnisse in '{db_path}'...")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True) # Existiert der Ordner für die Datenbank nicht, wird er erstellt

    # Bereinigte Daten zusätzlich als CSV sichern
    df.to_csv(csv_output_path, index=False, sep=";")

    # Verbindung zur SQLite-Datenbank herstellen und Tabelle schreiben
    with sqlite3.connect(db_path) as conn:
        df.to_sql("shipments", conn, if_exists="replace", index=False) # Die bereinigten Daten werden in die SQLite-Datenbanktabelle 'shipments' geschrieben, wobei vorhandene Daten ersetzt werden

    print("   -> Daten erfolgreich in SQL-Tabelle 'shipments' geladen!")


def run_pipeline() -> None:
    raw_file = "data/raw/shipments_raw.csv"
    clean_csv = "data/processed/shipments_clean.csv"
    database_file = "data/processed/logistics.db"

    raw_df = extract_data(raw_file)
    clean_df = transform_data(raw_df)
    load_data(clean_df, database_file, clean_csv)


if __name__ == "__main__":
    run_pipeline()
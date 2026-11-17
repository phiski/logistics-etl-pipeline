import pandas as pd
from src.pipeline import transform_data


def test_transform_data_cleansing():
    # Testdaten mit typischen Fehlern anlegen (Dublette, Kleinschreibung, ungültiges Gewicht)
    raw_df = pd.DataFrame({
        "shipment_id": ["SHP-1", "SHP-1", "SHP-2", "SHP-3"],
        "warehouse": ["dortmund", "dortmund", "HOLZWICKEDE", "Hamm"],
        "destination_country": ["Deutschland", "Deutschland", "GER", "NL"],
        "weight_kg": [10.0, 10.0, -5.0, None],
        "dispatch_time": [
            "2026-11-01 10:00:00",
            "2026-11-01 10:00:00",
            "2026-11-01 10:00:00",
            "2026-11-01 10:00:00",
        ],
        "delivery_time": [
            "2026-11-02 10:00:00",  # 24 Stunden -> pünktlich
            "2026-11-02 10:00:00",
            "2026-11-04 10:00:00",  # 72 Stunden -> verspätet
            "2026-11-02 22:00:00",  # 36 Stunden -> pünktlich
        ],
        "status": ["Delivered", "Delivered", "Delayed", "Delivered"],
    })

    clean_df = transform_data(raw_df)

    # 1. Wurde die Dublette entfernt? (Erwartet: 3 statt 4 Zeilen)
    assert len(clean_df) == 3

    # 2. Wurden die Lagernamen einheitlich formatiert?
    assert list(clean_df["warehouse"]) == ["Dortmund", "Holzwickede", "Hamm"]

    # 3. Wurden die Ländercodes auf ISO-Standard gebracht?
    assert list(clean_df["destination_country"]) == ["DE", "DE", "NL"]

    # 4. Wurden ungültige Gewichte (-5.0 und None) durch den Median (10.0) ersetzt?
    assert list(clean_df["weight_kg"]) == [10.0, 10.0, 10.0]

    # 5. Wurde die Verspätungs-Flag (> 48h) korrekt gesetzt?
    assert list(clean_df["is_delayed"]) == [False, True, False]
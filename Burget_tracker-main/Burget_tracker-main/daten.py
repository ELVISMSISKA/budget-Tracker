#=====================
#        Daten
#=====================
"""
Diese Modul ist für die Daten-Management zuständig.
Neue Transaktionen in CSV Datei speichern und dies wiedergeben.
"""

DATEINAME = "budget_daten.csv"


def speichere_transaktion(datum, typ, kategorie, betrag, beschreibung):
    """Speichert eine neue Transaktion in der CSV Datei"""
    
    # Prüfen, ob die Datei bereits existiert
    try:
        with open(DATEINAME, "r"):
            datei_existiert = True
    except FileNotFoundError:
        datei_existiert = False
    
    # Datei im Anhängemodus öffnen, falls nicht vorhanden, wird sie automatisch neu erstellt
    with open(DATEINAME, "a") as f:
        # Wenn die Datei neu ist - Überschrift schreiben
        if not datei_existiert:
            f.write("datum;typ;kategorie;betrag;beschreibung\n")
        
        # vollständige CSV-Zeile bauen und in die Datei schreiben
        zeile = f"{datum};{typ};{kategorie};{betrag};{beschreibung}\n"
        f.write(zeile)


def lade_transaktionen():
    """ Lädt alle Transaktionen aus der CSV Datei"""
    
    transaktionen = []  # Leere Liste für die Transaktionen
    
    # Datei öffnen und alle Zeilen einlesen
    try:
        with open(DATEINAME, "r") as f:
            zeilen = f.readlines()
    except FileNotFoundError:
        # Datei existiert nicht
        print(f"Die Datei '{DATEINAME}' wurde nicht gefunden.")
        return []
    
    # Erste Zeile ist Überschrift - überspringen
    for zeile in zeilen[1:]:
        # Leerzeichen und Zeilenumbruch entfernen, dann an ";" aufteilen
        teile = zeile.strip().split(";")
        
        # Prüfen ob Zeile vollständig ist (5 Felder erwartet)
        #Zusätzlicher Schutz, falls CSV-Datei beschädigt ist und so Beschädigung beseitigen. 
        #(Wenn CSV manuell geöffnet wurde und geändert wurde)

        if len(teile) != 5:
            print("Warnung: Unvollständige Zeile übersprungen")
            continue
        
        # Betrag sicher in float konvertieren
        try:
            betrag = float(teile[3])
        except ValueError:
            print(f"Warnung: Ungültiger Betrag '{teile[3]}' - Zeile übersprungen")
            continue
        
        # Dictionary aus der Zeile erstellen
        transaktion = {
            "datum": teile[0],
            "typ": teile[1],
            "kategorie": teile[2],
            "betrag": betrag,
            "beschreibung": teile[4]
        }
        
        # Transaktion zur Liste hinzufügen
        transaktionen.append(transaktion)
    
    # Die komplette Liste zurückgeben
    return transaktionen

#=====================
#Test-Modul:
#=====================

if __name__ == "__main__":
    # Test mit Beispieldaten - ohne Benutzereingaben
    test_daten = {
        "datum": "2025-12-11",
        "typ": "AUSGABE",
        "kategorie": "Lebensmittel",
        "betrag": 25.50,
        "beschreibung": "Wochenmarkt Einkaufen"
    }
    
    print("Speichere Test-Transaktion...")
    speichere_transaktion(**test_daten)
    print("✓ Transaktion gespeichert!")
    
    print("\nAlle Transaktionen:")
    trans = lade_transaktionen()
    for t in trans:
        print(t)


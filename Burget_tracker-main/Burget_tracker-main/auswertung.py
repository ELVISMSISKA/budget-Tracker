#=====================
#    Auswertung
#=====================


"""
Auswertung der Transaktionen.

Funktionen: 
    - Monatsübersicht
    - Statistik der Kategorien  
    - Ausgabe alles Transaktionen
"""

def monatsuebersicht(transaktionen):
    """
    Gibt Gesamteinnahmen, Ausgaben und Saldo des Monats an. 
    """
    #Validierung von Transaktionen, ob es überhaupt Transkationen gibt.
    if not transaktionen: 
        print ("Es sind keine Transaktionen vorhanden.")
        return
    
    #Beschreibung
    print ('\n=== Monatsübersicht ===')

    #Jahr validieren
    while True:
        jahr_input = input("Jahr eingeben (YYYY): ").strip()
        try:
            jahr = int(jahr_input)
            if 1000 <= jahr <= 9999:
                break
            print("Jahr muss zwischen 1000 und 9999 liegen.")
        except ValueError:
            print("Ungültiges Jahr! Bitte eine Zahl eingeben.")

    # Monat validieren 
    while True:
        monat_input = input("Monat eingeben (MM): ").strip()
        try:
            monat = int(monat_input)
            if 1 <= monat <= 12:
                break
            print("Monat muss zwischen 1 und 12 liegen.")
        except ValueError:
            print("Ungültiger Monat! Bitte eine Zahl eingeben.")

    #Formatierung ins richtige Datenformat
    dat = f"{jahr}-{monat:02d}" # ---> :02d bedeutet, das die Eingabe Monat = 1 --> 01 gemacht wird, damit das Programm korrekt versteht

    #Startwert
    gesamteinnahmen = 0.0
    gesamtausgaben = 0.0
    anzahl_trans = 0.0

    #Überspringt alle Transaktionen die nicht im abgefragten Jahr und Monat sind.
    for t in transaktionen: 
        datum = t.get('datum', '')
        if len(datum) < 7 or datum[:7] != dat: #prüfe Länge und vergleiche das Präfix per Slicing
            continue

        betrag = float(t.get("betrag", 0.0))    # Betrag wird abgerufen aus Dictionary
        typ = t.get("typ", "").upper()          # Typ wird abgerufen in Grossbuchstaben

        #Gesamteinnahme für jeweilige Typ aufsummieren
        if typ == "EINNAHME":
            gesamteinnahmen += betrag
        elif typ == "AUSGABE":
            gesamtausgaben += betrag

        anzahl_trans += 1

    print(f"\nMonat: {jahr}-{monat}")
    print(f"Anzahl Transaktionen: {anzahl_trans}")
    print(f"Gesamteinnahmen: {gesamteinnahmen:.2f} CHF")
    print(f"Gesamtausgaben:  {gesamtausgaben:.2f} CHF")
    print(f"Saldo (Einnahmen - Ausgaben): {gesamteinnahmen - gesamtausgaben:.2f} CHF\n")


def kategorien_statistik(transaktionen):
    """
    Zeigt eine Statistik nach Kategorien an.

    Ablauf:
    - Benutzer wählt, ob nur EINNAHMEN, nur AUSGABEN oder ALLE
    - Summiert die Beträge pro Kategorie
    - Gibt das Ergebnis aus
    """
    #Validierung von Transaktionen, ob es überhaupt Transkationen gibt.
    if not transaktionen:
        print("Es sind keine Transaktionen vorhanden.")
        return

    #Beschreibung
    print("\n=== Kategorienstatistik ===")
    print("1: Nur EINNAHMEN")
    print("2: Nur AUSGABEN")
    print("3: Alle (EINNAHMEN und AUSGABEN)")

    wahl = input("Auswahl eingeben: ").strip()

    if wahl == "1":
        typ_filter = "EINNAHME"
        print_typ = "EINNAHMEN"
    elif wahl == "2":
        typ_filter = "AUSGABE"
        print_typ = "AUSGABEN"
    elif wahl == "3":
        typ_filter = "ALLE"
        print_typ = "ALLE"
    else:
        print("Ungültige Auswahl.")
        return

    summen_pro_kategorie = {}

    # Auswahl Valdierung
    for t in transaktionen:
        typ = t.get("typ", "").upper()
        if typ_filter != "ALLE" and typ != typ_filter: #schaut ob einnahme oder Ausgabe gewählt wurde
            continue

        kategorie = t.get("kategorie", "")  # Kategorie wird abgerufen aus Dictionary
        betrag = float(t.get("betrag", 0.0)) # Betrag wird abgerufen aus Dictionary

        # Bei EINNAHMEN positiv, bei AUSGABEN ebenfalls als positiver Betrag aufsummieren
        summen_pro_kategorie[kategorie] = summen_pro_kategorie.get(kategorie, 0.0) + betrag
        # summen_pro_kategorie[kategorie]

    print(f"\nKategorienstatistik ({print_typ}):")
    if not summen_pro_kategorie:
        print("Keine passenden Transaktionen gefunden.")
        return

    for kat, summe in summen_pro_kategorie.items():
        print(f"- {kat}: {summe:.2f} CHF")
    print()


def alle_transaktionen_ausgeben(transaktionen):
    """
    Gibt alle Transaktionen formatiert in der Konsole aus.

    Zeigt:
    - Datum
    - Typ
    - Kategorie
    - Betrag
    - Beschreibung
    """

    print("\n=== Alle Transaktionen ===")

    if not transaktionen:
        print("Es sind noch keine Transaktionen erfasst.")
        return

    #Sortieren nach Datum
    def get_datum(t):
        return t.get("datum", "")
    
    sortierte_transaktionen = sorted(transaktionen, key=get_datum)

    #Header
    print(f"{'Datum':<12} {'Typ':<10} {'Kategorie':<20} {'Betrag':>10}  Beschreibung")
    print("-" * 70)

    #alle Transaktionen ausgeschrieben in Tabellenform
    for t in sortierte_transaktionen:
        datum = t.get("datum", "")
        typ = t.get("typ", "")
        kategorie = t.get("kategorie", "")
        betrag = float(t.get("betrag", 0.0))
        beschreibung = t.get("beschreibung", "")

        print(f"{datum:<12} {typ:<10} {kategorie:<20} {betrag:>10.2f}  {beschreibung}")

    print()



#=====================
#Test-Modul:
#=====================

if __name__ == "__main__":
    # Testdaten zum Ausprobieren
    test_transaktionen = [
        {
            "datum": "2025-01-05",
            "typ": "EINNAHME",
            "kategorie": "Lohn",
            "betrag": 3500.00,
            "beschreibung": "Januarlohn"
        },
        {
            "datum": "2025-01-10",
            "typ": "AUSGABE",
            "kategorie": "Miete",
            "betrag": 1200.00,
            "beschreibung": "Wohnungsmiete"
        },
        {
            "datum": "2025-01-12",
            "typ": "AUSGABE",
            "kategorie": "Lebensmittel",
            "betrag": 150.50,
            "beschreibung": "Wocheneinkauf"
        },
        {
            "datum": "2025-02-01",
            "typ": "AUSGABE",
            "kategorie": "Transport",
            "betrag": 80.00,
            "beschreibung": "Monatsabo"
        },
    ]

    print("=== TEST: Alle Transaktionen ===")
    alle_transaktionen_ausgeben(test_transaktionen)

    print("=== TEST: Monatsübersicht ===")
    # Hier wirst du nach Jahr und Monat gefragt (z.B. 2025 und 01)
    monatsuebersicht(test_transaktionen)

    print("=== TEST: Kategorienstatistik ===")
    # Hier wirst du gefragt: 1/2/3 (Einnahmen/Ausgaben/Alle)
    kategorien_statistik(test_transaktionen)
#=====================
#    Hauptprogramm
#=====================

"""
Hauptprogramm für den Budget-Tracker.

Verwendete Module:
- eingabe.py      -> Eingabe & Validierung von Transaktionen
- daten.py        -> Speichern & Laden der CSV-Datei
- auswertung.py   -> Auswertungen (Monatsübersicht, Kategorien, Ausgabe)
"""

import eingabe
import daten
import auswertung


def menue_anzeigen():
    """
    Zeigt das Hauptmenü an und gibt die Auswahl des Benutzers zurück.
    """
    print("\n===== BUDGET-TRACKER =====")
    print("1: Neue Transaktion erfassen")
    print("2: Monatsübersicht anzeigen")
    print("3: Kategorienstatistik anzeigen")
    print("4: Alle Transaktionen anzeigen")
    print("5: Speichern & Beenden")

    auswahl = input("Auswahl eingeben: ").strip()
    return auswahl


def main():
    """
    Hauptablauf des Programms:

    - vorhandene Transaktionen aus der CSV-Datei laden falls existiert sonst eine erstellen
    - Menü in einer Schleife anzeigen
    - Benutzeraktionen ausführen
    - neue Transaktionen am Ende speichern
    """

    # 1) Vorhandene Transaktionen laden (falls Datei existiert)
    transaktionen = daten.lade_transaktionen()
    # Liste nur für Transaktionen, die in dieser Sitzung NEU erfasst werden
    neue_transaktionen = []

    print("Willkommen im Budget-Tracker!")

    # 2) Endlosschleife für das Menü
    while True:
        auswahl = menue_anzeigen()

        if auswahl == "1":
            # Neue Transaktion erfassen
            print("\n--- Neue Transaktion erfassen ---")
            neue = eingabe.eingabe_transaktion()

            # zur Gesamtliste hinzufügen
            transaktionen.append(neue)
            # separat merken, dass diese noch gespeichert werden muss
            neue_transaktionen.append(neue)

        elif auswahl == "2":
            # Monatsübersicht anzeigen
            auswertung.monatsuebersicht(transaktionen)

        elif auswahl == "3":
            # Kategorienstatistik anzeigen
            auswertung.kategorien_statistik(transaktionen)

        elif auswahl == "4":
            # Alle Transaktionen anzeigen
            auswertung.alle_transaktionen_ausgeben(transaktionen)

        elif auswahl == "5":
            # Neue Transaktionen speichern und Programm beenden
            print("\nSpeichere neue Transaktionen...")

            if not neue_transaktionen:
                print("Es wurden keine neuen Transaktionen erfasst.")
            else:
                for t in neue_transaktionen:
                    daten.speichere_transaktion(
                        t["datum"],
                        t["typ"],
                        t["kategorie"],
                        t["betrag"],
                        t["beschreibung"]
                    )
                print(f"{len(neue_transaktionen)} neue Transaktion(en) gespeichert.")

            print("Programm wird beendet. Auf Wiedersehen!")
            break

        else:
            print("Ungültige Eingabe – bitte eine Zahl von 1 bis 5 eingeben.")


# Startpunkt des Programms
if __name__ == "__main__":
    main()

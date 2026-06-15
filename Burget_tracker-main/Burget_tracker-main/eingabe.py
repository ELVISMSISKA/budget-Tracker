#=====================
#       EINGABE
#      eingabe.py
#=====================
"""
Alle Eingaben für Transaktionen werde hier definiert und valdiert. 
(Datum, Typ, Kategorie, Betrag, Beschreibung)
"""


import datetime

#Konstanten:
#Einnahmen(wurde im Vorfeld schon überlegt und festgehalten):
EINNAHME_KATEGORIEN = ["Lohn", "Nebenjob", "Geschenke", "Sonstige_Einnahmen"]


#Ausgaben(wurde im Vorfeld schon überlegt und festgehalten):
AUSGABE_KATEGORIEN = [
     "Miete",
     "Nebenkosten",
     "Lebensmittel",
     "Transport",
     "Krankenkasse",
     "Freizeit",
     "Shopping",
     "Haushalt",
     "Sonstige_Ausgaben",
 ]
 
#=====================
#Eingabefunktionen
#=====================


#Datum --------> schauen obs mir so gefällt wegen Format oder ändern
def eingabe_datum():
    """fragt Datum ab und prüft auf Format und Gültigkeit."""

    while True: 
        datum = input("Datum eingeben (YYYY-MM-DD): ")
        
        try:
            datetime.datetime.strptime(datum, "%Y-%m-%d")
            return datum
         
        except ValueError:
            print("Ungültiges Datum!")
            

#Typ
def eingabe_typ():
    """Fragt Typ der Transkation ab und valdiert."""
    
    while True:
        typ = input("Typ eingeben (EINNAHME / AUSGABE): ").strip().upper()
        if typ in ["EINNAHME", "AUSGABE"]:
            return typ
        else:
            print("Ungültiger Typ!")


#Kategorie
def eingabe_kategorie(typ):
    """Fragt Kategorie ab passend Typs(Kategorien oben festgehalten)."""

    if typ == "EINNAHME": #wird definiert welche Kategorie 
        kategorien = EINNAHME_KATEGORIEN
    else:
        kategorien = AUSGABE_KATEGORIEN
        
    print("\nVerfügbare Kategorien:") #definierte Kategorie wird angezeigt
    zahl = 1
    for kat in kategorien:
        print(zahl, ":", kat)
        zahl = zahl + 1
        
    # Auswahl tätigen und valdieren
    while True:
        auswahl = input("Kategorie wählen (Nummer oder Name): ")
        
        # Wenn Nummer eingegeben wurde 
        if auswahl.isdigit():
            nummer = int(auswahl)
            if 1 <= nummer <= len(kategorien):
                return kategorien[nummer -1]
            else:
                print("Ungültige Nummer!")
            
        # Wenn Name eingegeben wurde
        else:
            if auswahl in kategorien:
                return auswahl
            else:
                print("Ungültige Kategorie!")


#Betrag
def eingabe_betrag():
    """Fragt nach dem Geldbetrag und validiert auf float und obs positiv ist."""

    while True:
        eingabe = input("Betrag eingeben (z.B. 21.95): ")
        
        try:
            betrag = float(eingabe)
            if betrag > 0:
                return betrag
            else:
                print("Betrag muss positiv sein!")
                
        except ValueError:
            print("Ungültiger Betrag! ")



#Beschreibung
def eingabe_beschreibung():
    """Beschreibung wird abgefragt und validiert dies auf Semikolon (CSV-Format beibehalten)"""
    
    while True:
        beschreibung = input("Beschreibung eingeben (kein ';' verwenden): ")
        
        if ";" in beschreibung:
            print("Beschreibung darf kein ';' enthalten!")
        else:
            return beschreibung


#=====================
#Transaktion erfassen
#=====================
def eingabe_transaktion():
    """
    Neue vollständige Tranksaktion wird hier erfasst. Eingabefunktionen werden
    aufgerufen und verwendet: 
        Ablauf: 
            - Datum
            - Typ eingeben
            - passende Kategorie zum Typ wählen
            - Gelbetrag eingeben
            - Beschreibung eingeben
    
    Rückgabe in Dictionary für Leserlichkeit und Verständnis
    """


    print("\n--- Neue Transaktion erfassen ---")
    
    datum = eingabe_datum()
    typ = eingabe_typ()
    kategorie = eingabe_kategorie(typ)
    betrag = eingabe_betrag()
    beschreibung = eingabe_beschreibung()
    
    
    transaktion = {
        "datum": datum,
        "typ": typ,
        "kategorie": kategorie,
        "betrag": betrag,
        "beschreibung": beschreibung,
    }
    
    print("\nTransaktion erfasst:")
    print(transaktion)
    
    return transaktion   


#=====================
#.    Test_Modul
#=====================
#eingabe_datum()

#eingabe_typ()

#typ = eingabe_typ()
#eingabe_kategorie(typ)     #--> Kann nur getestet werden wen eingabe_typ() vorher ausgeführt wurde.

# eingabe_betrag()

# eingabe_betrag()


def main():
    eingabe_transaktion()

if __name__ == '__main__':
   main()

                 
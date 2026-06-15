from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request

import daten
from eingabe import AUSGABE_KATEGORIEN, EINNAHME_KATEGORIEN

app = Flask(__name__, static_folder="static", template_folder="templates")


def validate_transaction(data):
    if not isinstance(data, dict):
        return False, "Ungültiges Transaktionsformat."

    datum = str(data.get("datum", "")).strip()
    typ = str(data.get("typ", "")).strip().upper()
    kategorie = str(data.get("kategorie", "")).strip()
    beschreibung = str(data.get("beschreibung", "")).strip()
    betrag = data.get("betrag")

    if not datum or not typ or not kategorie or not beschreibung or betrag is None:
        return False, "Alle Felder sind erforderlich."

    try:
        datetime.strptime(datum, "%Y-%m-%d")
    except ValueError:
        return False, "Datum muss im Format YYYY-MM-DD sein."

    if typ not in ["EINNAHME", "AUSGABE"]:
        return False, "Typ muss EINNAHME oder AUSGABE sein."

    if typ == "EINNAHME":
        valid_categories = EINNAHME_KATEGORIEN
    else:
        valid_categories = AUSGABE_KATEGORIEN

    if kategorie not in valid_categories:
        return False, f"Ungültige Kategorie für {typ}."

    try:
        betrag = float(betrag)
        if betrag <= 0:
            return False, "Betrag muss größer als 0 sein."
    except (TypeError, ValueError):
        return False, "Ungültiger Betrag."

    if ";" in beschreibung:
        return False, "Beschreibung darf kein Semikolon enthalten."

    return True, {
        "datum": datum,
        "typ": typ,
        "kategorie": kategorie,
        "betrag": betrag,
        "beschreibung": beschreibung,
    }


def build_monthly_summary(transactions, year, month):
    prefix = f"{year}-{month:02d}"
    totaleinnahmen = 0.0
    totaleausgaben = 0.0
    anzahl = 0

    for t in transactions:
        datum = t.get("datum", "")
        if not datum.startswith(prefix):
            continue

        typ = str(t.get("typ", "")).upper()
        betrag = float(t.get("betrag", 0.0))

        if typ == "EINNAHME":
            totaleinnahmen += betrag
        elif typ == "AUSGABE":
            totaleausgaben += betrag

        anzahl += 1

    return {
        "jahr": year,
        "monat": month,
        "anzahl_transaktionen": anzahl,
        "gesamteinnahmen": round(totaleinnahmen, 2),
        "gesamtausgaben": round(totaleausgaben, 2),
        "saldo": round(totaleinnahmen - totaleausgaben, 2),
    }


def build_category_stats(transactions, typ_filter):
    summen = {}
    for t in transactions:
        typ = str(t.get("typ", "")).upper()
        if typ_filter != "ALLE" and typ != typ_filter:
            continue

        kategorie = t.get("kategorie", "")
        betrag = float(t.get("betrag", 0.0))
        summen[kategorie] = summen.get(kategorie, 0.0) + betrag

    return [{"kategorie": k, "summe": round(v, 2)} for k, v in sorted(summen.items(), key=lambda item: item[1], reverse=True)]


@app.route("/")
def index():
    return render_template(
        "index.html",
        einkommen=EINNAHME_KATEGORIEN,
        ausgaben=AUSGABE_KATEGORIEN,
    )


@app.route("/api/transactions", methods=["GET"])
def api_transactions():
    transactions = daten.lade_transaktionen()
    return jsonify(transactions)


@app.route("/api/transactions", methods=["POST"])
def api_add_transaction():
    data = request.get_json(silent=True)
    valid, result = validate_transaction(data)
    if not valid:
        return jsonify({"error": result}), 400

    daten.speichere_transaktion(
        result["datum"],
        result["typ"],
        result["kategorie"],
        result["betrag"],
        result["beschreibung"],
    )
    return jsonify({"message": "Transaktion gespeichert."}), 201


@app.route("/api/monthly-summary", methods=["GET"])
def api_monthly_summary():
    year = request.args.get("year")
    month = request.args.get("month")

    if not year or not month:
        return jsonify({"error": "Jahr und Monat sind erforderlich."}), 400

    try:
        year = int(year)
        month = int(month)
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Ungültiges Jahr oder Monat."}), 400

    transactions = daten.lade_transaktionen()
    summary = build_monthly_summary(transactions, year, month)
    return jsonify(summary)


@app.route("/api/category-stats", methods=["GET"])
def api_category_stats():
    typ = request.args.get("type", "ALLE").upper()
    if typ not in ["EINNAHME", "AUSGABE", "ALLE"]:
        return jsonify({"error": "Typ muss EINNAHME, AUSGABE oder ALLE sein."}), 400

    transactions = daten.lade_transaktionen()
    stats = build_category_stats(transactions, typ)
    return jsonify({"type": typ, "stats": stats})


if __name__ == "__main__":
    app.run(debug=True)

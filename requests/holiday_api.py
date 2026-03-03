"""
Practice: API keys – Holiday API
- Ruft verfügbare Länder ab und lässt den Nutzer eines wählen.
- Zeigt alle Feiertage des Vorjahres für das gewählte Land (Name + Datum).
API-Dokumentation: https://holidayapi.com/docs
"""
import os
from datetime import datetime
import requests

BASE_URL = "https://holidayapi.com/v1"


def get_api_key():
    """API-Key aus Umgebungsvariable oder Benutzereingabe."""
    key = os.environ.get("HOLIDAYAPI_KEY", "").strip()
    if key:
        return key
    return input("Enter your Holiday API key: ").strip()


def ordinal(n):
    """Tag als Ordinalzahl: 1 -> 1st, 2 -> 2nd, 22 -> 22nd."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def format_holiday_date(date_str):
    """Datum-String (YYYY-MM-DD) in 'Weekday, Month DDth' umwandeln."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        day_ord = ordinal(d.day)
        return d.strftime(f"%A, %B {day_ord}")
    except (ValueError, TypeError):
        return date_str


def _parse_response(r, context="Request"):
    """JSON parsen und verständliche Fehlermeldung bei API-Fehlern."""
    try:
        data = r.json()
    except Exception:
        raise RuntimeError(
            f"{context} failed: HTTP {r.status_code}. Response: {r.text[:300]}"
        )
    if not r.ok:
        err = (
            data.get("error")
            or data.get("message")
            or data.get("status")
            or r.text
            or f"HTTP {r.status_code}"
        )
        raise RuntimeError(f"{context} failed: {err}")
    return data


def fetch_countries(key):
    """Alle verfügbaren Länder von der API abrufen."""
    r = requests.get(
        f"{BASE_URL}/countries", params={"key": key}, timeout=30
    )
    data = _parse_response(r, "Countries")
    if data.get("error"):
        raise RuntimeError(f"Countries: {data.get('error')}")
    countries = data.get("countries") or data.get("country") or []
    if isinstance(countries, dict):
        # z.B. {"US": {"name": "United States"}, ...} oder {"US": "United States"}
        out = []
        for code, val in countries.items():
            if isinstance(val, dict):
                out.append({"code": code, "name": val.get("name", val.get("country", code))})
            else:
                out.append({"code": code, "name": str(val)})
        countries = out
    return countries


def fetch_holidays(key, country_code, year):
    """Feiertage für ein Land und Jahr abrufen."""
    r = requests.get(
        f"{BASE_URL}/holidays",
        params={"key": key, "country": country_code, "year": year},
        timeout=30,
    )
    data = _parse_response(r, "Holidays")
    if data.get("error"):
        raise RuntimeError(f"Holidays: {data.get('error')}")
    return data.get("holidays") or data.get("holiday") or []


def country_list_to_map(countries):
    """Liste von Länder-Objekten in ein name -> code Mapping umwandeln."""
    name_to_code = {}
    for c in countries:
        if not isinstance(c, dict):
            continue
        name = c.get("name") or c.get("country") or c.get("country_name") or ""
        code = c.get("code") or c.get("country_code") or c.get("iso") or ""
        if not code and isinstance(c.get("codes"), dict):
            code = c["codes"].get("alpha-2", "")
        if isinstance(code, dict):
            code = code.get("alpha-2", "")
        if name and code:
            name_to_code[name.strip()] = str(code).strip()
    return name_to_code


def main():
    key = get_api_key()
    if not key:
        print("No API key provided. Set HOLIDAYAPI_KEY or enter your key.")
        print("Get a free key at https://holidayapi.com")
        return

    try:
        raw_countries = fetch_countries(key)
    except RuntimeError as e:
        print(e)
        return

    name_to_code = country_list_to_map(raw_countries)
    if not name_to_code:
        # Fallback: Nur Codes verwenden, wenn API nur Codes zurückgibt
        for c in raw_countries:
            if isinstance(c, dict):
                code = c.get("code") or c.get("country_code")
                name = c.get("name") or c.get("country") or code
                if code:
                    name_to_code[name or code] = str(code)
        if not name_to_code:
            print("No countries returned from API. Check your key and API docs.")
            return

    names = sorted(name_to_code.keys())
    print("Available countries:\n")
    for name in names:
        print(name)
    print()

    country_input = input("Enter a country: ").strip()
    if not country_input:
        print("No country entered.")
        return

    # Exakte oder case-insensitive Suche; Fallback: Name beginnt mit Eingabe
    country_code = name_to_code.get(country_input)
    if not country_code:
        low = country_input.lower()
        for name, code in name_to_code.items():
            if name.lower() == low:
                country_code = code
                break
        if not country_code:
            for name, code in name_to_code.items():
                if name.lower().startswith(low) or low in name.lower():
                    country_code = code
                    break
    if not country_code:
        print(f"Country not found: '{country_input}'. Use a name from the list above.")
        return

    last_year = datetime.now().year - 1
    try:
        holidays = fetch_holidays(key, country_code, last_year)
    except RuntimeError as e:
        print(e)
        return

    if not holidays:
        print(f"No holidays found for {country_input} in {last_year}.")
        return

    # Nach Datum sortieren
    def sort_key(h):
        d = h.get("date") or h.get("observed") or ""
        return d

    holidays_sorted = sorted(holidays, key=sort_key)

    print(f"\nList of holidays in the last year ({last_year}):")
    for h in holidays_sorted:
        name = h.get("name") or h.get("title") or "Unnamed"
        date_str = h.get("date") or h.get("observed") or ""
        formatted = format_holiday_date(date_str)
        print(f"{name} ({formatted})")


if __name__ == "__main__":
    main()

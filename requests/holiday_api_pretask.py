"""
Pre-Task: Holiday API – Feiertage für das *nächste* Jahr abrufen.
- Zeigt den HTTP-Statuscode und die JSON-Antwort.
- Auf vielen Free-Tarifen liefert die API für zukünftige Jahre 402 (Payment Required)
  oder einen Fehler – das ist die „Problemstellung“ zum Debuggen.
"""
import os
import json
import requests

def main():
    key = os.environ.get("HOLIDAYAPI_KEY", "").strip() or input("Enter your Holiday API key: ").strip()
    if not key:
        print("No API key provided.")
        return

    next_year = __import__("datetime").datetime.now().year + 1
    url = "https://holidayapi.com/v1/holidays"
    params = {"key": key, "country": "US", "year": next_year}

    print(f"Request: GET {url} with country=US, year={next_year}\n")
    r = requests.get(url, params=params)

    print(f"HTTP status code: {r.status_code}")
    print("Meaning: ", end="")
    if r.status_code == 200:
        print("OK – Anfrage erfolgreich.")
    elif r.status_code == 402:
        print("Payment Required – z.B. Free-Tarif enthält keine Daten für zukünftige Jahre.")
    elif r.status_code == 401:
        print("Unauthorized – ungültiger oder fehlender API-Key.")
    elif r.status_code == 403:
        print("Forbidden – Zugriff verweigert.")
    else:
        print("Siehe Holiday API Docs für Status-Codes.")
    print()

    try:
        data = r.json()
        print("JSON response:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
        if len(json.dumps(data)) > 2000:
            print("... (truncated)")
    except Exception:
        print("Response (raw):", r.text[:500])

if __name__ == "__main__":
    main()

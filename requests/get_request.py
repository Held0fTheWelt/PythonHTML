"""
Task 1: GET-Request mit Parametern (name, color).
Verwendet requests.get() mit dem params-Argument.
Speichert die HTML-Antwort automatisch in _static/get_me.html.
"""
import os
import requests

URL = "https://learningserver.masterschool.com/http-basics/get-me"
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "_static")


def main():
    name = input("Enter name: ")
    color = input("Enter color: ")

    response = requests.get(URL, params={"name": name, "color": color})
    print("Output:", flush=True)
    print(response.text, flush=True)

    os.makedirs(STATIC_DIR, exist_ok=True)
    filepath = os.path.join(STATIC_DIR, "get_me.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Gespeichert: {filepath}", flush=True)


if __name__ == "__main__":
    main()

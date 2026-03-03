"""
Task 2: POST-Request mit Formulardaten (username, password).
Verwendet requests.post() mit dem data-Argument für Form-Daten.
Korrekte Anmeldedaten: Johana / PostingIsCool
Speichert die HTML-Antwort automatisch in _static/post_me.html.
"""
import os
import requests

URL = "https://learningserver.masterschool.com/http-basics/post-me"
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "_static")


def main():
    username = input("Enter username: ")
    password = input("Enter password: ")

    response = requests.post(
        URL,
        data={"username": username, "password": password},
    )
    print("Output:", flush=True)
    print(response.text, flush=True)

    os.makedirs(STATIC_DIR, exist_ok=True)
    filepath = os.path.join(STATIC_DIR, "post_me.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Gespeichert: {filepath}", flush=True)


if __name__ == "__main__":
    main()

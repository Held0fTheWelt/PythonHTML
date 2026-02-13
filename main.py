import requests

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return response.status_code

def get_input_url():
    url = input("Enter URL: ")
    return url

def main():
    print(get_html(get_input_url()))


if __name__ == "__main__":
    main()


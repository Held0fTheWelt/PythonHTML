import requests


def save_to_file(text, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(text)

def get_response(url):
    response = requests.get(url)
    return response

def get_filename():
    filename = input("Enter the filename: ")
    return filename

def get_input_url():
    url = input("Enter URL: ")
    return url

def main():
    response = get_response(get_input_url())

    if response.status_code != 200:
        print(f"{response.status_code}: {response.text}")
        return

    save_to_file(response.text, get_filename())

if __name__ == "__main__":
    main()


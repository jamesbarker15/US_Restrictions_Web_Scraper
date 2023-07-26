import requests
import selectorlib

URL = "https://ofac.treasury.gov/sanctions-programs-and-country-information"
HEADERS = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["sanctions"]
    return value


def save_sanctions_to_file_refresh(sanctions):
    with open('refresh_sanctions.txt', 'w') as file:
        file.write("\n".join(sanctions))


def compare_sanctions(file_path1, file_path2):
    with open(file_path1, 'r') as file1:
        content1 = file1.readlines()

    with open(file_path2, 'r') as file2:
        content2 = file2.readlines()

    # Compare line by line
    if len(content1) != len(content2):
        return False

    for line1, line2 in zip(content1, content2):
        if line1 != line2:
            return False

    return True


refresh_sanctions = []

if __name__ == "__main__":
    file_path1 = 'sanctions.txt'
    file_path2 = 'refresh_sanctions.txt'
    scraped = scrape(URL)
    extracted = extract(scraped)
    countries = extracted.split(",")
    for c in countries:
        refresh_sanctions.append(c.strip())
save_sanctions_to_file_refresh(refresh_sanctions)

if compare_sanctions('sanctions.txt', 'refresh_sanctions.txt'):
    print("The sanctions have not changed.")
else:
    print("The sanctions have changed.")



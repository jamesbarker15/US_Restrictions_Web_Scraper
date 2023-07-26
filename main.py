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

def save_sanctions_to_file(sanctions):
    with open('sanctions.txt', 'w') as file:
        file.write("\n".join(sanctions))


current_sanctions = []

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    countries = extracted.split(",")
    for c in countries:
        current_sanctions.append(c.strip())

save_sanctions_to_file(current_sanctions)



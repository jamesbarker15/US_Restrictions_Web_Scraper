import requests
import selectorlib
import smtplib
import ssl
import os

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


def compare_sanctions(sanctions, refresh_sanctions):
    with open(sanctions, 'r') as file1:
        content1 = file1.readlines()

    with open(refresh_sanctions, 'r') as file2:
        content2 = file2.readlines()

    # Compare line by line
    if len(content1) != len(content2):
        return False

    for line1, line2 in zip(content1, content2):
        if line1 != line2:
            return False

    return True

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    receiver = "james.barker132@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent!")


def overwrite_sanctions(new_sanctions):
    with open('sanctions.txt', 'w') as file:
        file.write("\n".join(new_sanctions))


refresh_sanctions = []

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    countries = extracted.split(",")
    for c in countries:
        refresh_sanctions.append(c.strip())
save_sanctions_to_file_refresh(refresh_sanctions)

if compare_sanctions('sanctions.txt', 'refresh_sanctions.txt'):
    send_email(message="The sanctions have not changed.")
    print("The sanctions have not changed.")
else:
    send_email(message="The sanctions have changed!")
    overwrite_sanctions(refresh_sanctions)
    print("*****The sanctions have changed*****")



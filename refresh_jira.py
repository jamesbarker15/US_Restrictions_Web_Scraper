import requests
import selectorlib
from jira import JIRA
from keys import KEY, EMAIL

#github.com/jamesbarker15
URL = "https://ofac.treasury.gov/sanctions-programs-and-country-information"
HEADERS = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
refresh_sanctions = []


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

    if len(content1) != len(content2):
        return False

    for line1, line2 in zip(content1, content2):
        if line1 != line2:
            return False

    return True


def overwrite_sanctions(new_sanctions):
    with open('sanctions.txt', 'w') as file:
        file.write("\n".join(new_sanctions))


def create_jira_issue():
    jira_connection = JIRA(basic_auth=(EMAIL, KEY),
                           server="https://jamesbarker.atlassian.net")
    issue_dict = {
        'project': {'key': 'CP'},
        'summary': 'The US Sanctions have changed.',
        'description': 'Please check https://ofac.treasury.gov/'
                       'sanctions-programs-and-country-information as the '
                       'sanctions have changed..',
        'issuetype': {'name': 'Task'},
        'priority': {'name': 'High'}
    }
    new_issue = jira_connection.create_issue(fields=issue_dict)
    return new_issue


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    countries = extracted.split(",")
    for c in countries:
        refresh_sanctions.append(c.strip())
save_sanctions_to_file_refresh(refresh_sanctions)

if compare_sanctions('sanctions.txt', 'refresh_sanctions.txt'):
    print("The sanctions have not changed.")
else:
    new_issue = create_jira_issue()
    overwrite_sanctions(refresh_sanctions)
    print("The sanctions have changed.")



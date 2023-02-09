import pandas as pd
from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.forbes.com/lists/global2000/?sh=3c158f5d5ac0")

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find(id="table")
company_names = soup.find_all("div", class_="organizationName")

# df = pd.DataFrame()
data = [[],[], []]

i = 1
for element in company_names:
    print(i)
    i += 1
    data[0].append(element.previous_sibling.text)
    data[1].append(element.text)

    try:
        company_url = element.parent['href']
        company_page = requests.get(company_url)
        company_soup = BeautifulSoup(company_page.content, "html.parser")
        industry = company_soup.find("div", class_="listuser-block__item").contents[1].text
        data[2].append(industry)
    except KeyError:
        try:
            print('trying keyerror')
            company_url = "https://www.forbes.com/companies/" + element.text.lower().replace(" ", "-") + "/?list=global2000"
            print(company_url)
            company_page = requests.get(company_url)
            company_soup = BeautifulSoup(company_page.content, "html.parser")
            industry = company_soup.find("div", class_="listuser-block__item").contents[1].text
            data[2].append(industry)
        except:
            print("KEY ERROR on " + element.text)
            data[2].append("")


df = pd.DataFrame(data)
df = df.T
df.columns = ['Rankings', 'Company', 'Industry']
df.to_csv('results.csv', sep='\t', index=False)

print("DONE!")
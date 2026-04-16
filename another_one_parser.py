import requests
from bs4 import BeautifulSoup
import csv

url = 'https://news.ycombinator.com/'

def parse_link(max_links = 20):

    data = []
    page = 1

    while(len(data) < max_links):
        if page == 1:
            page_url = url
        else:
            page_url = f"{url}?p={page}"
        response = requests.get(page_url, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            break
        else:

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all('tr', class_ = 'athing')

            for link in links:

                if len(data) > max_links:
                    break

                title_tag = link.find('span', class_ = 'titleline').find('a')
                title = title_tag.text if title_tag else "Названия нет"

                article_link_tag = link.find('span', class_ = 'sitebit comhead').find('a')
                article_link = article_link_tag.text if article_link_tag else "Ссылки на статью нет"

                next_row = link.find_next_sibling('tr')
                if next_row:
                    score_tag = next_row.find('span', class_='score')
                    if score_tag:
                        score = score_tag.text  # .text, а не .get('score')!
                    else:
                        score = "Оценки нет"
                else:
                    score = "Оценки нет"
                data.append (
                    {
                        'title': title,
                        'article': article_link,
                        'score': score
                    }
                )
            page += 1
        
        return data

def save_to_csv(data):
    with open('links.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'article', 'score'])  
        writer.writeheader()
        writer.writerows(data)

def main():
    data = parse_link()
    save_to_csv(data)

if __name__ == "__main__":
    main()

                

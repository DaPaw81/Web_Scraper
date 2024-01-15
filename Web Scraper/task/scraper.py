from bs4 import BeautifulSoup
import requests
import os
import string

def status_code(response):
    if response.status_code == 200:
        return True
    else:
        print(f'The URL returned {response.status_code}!')
        exit()

def stage_4(url, art_type, folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    response = requests.get(url)
    if not status_code(response):
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        article_type = article.find('span', {'data-test': 'article.type'})
        if article_type and article_type.get_text().strip() == art_type:
            link = article.find('a', {'data-track-action': 'view article'})
            if link and 'href' in link.attrs:
                article_url = f"https://www.nature.com{link['href']}"
                article_page = requests.get(article_url)
                article_soup = BeautifulSoup(article_page.content, 'html.parser')

                body = article_soup.find('p', {'class': 'article__teaser'})
                if body:
                    title = link.get_text().strip()
                    filename = ''.join(ch if ch not in string.punctuation else '' for ch in title)
                    filename = filename.replace(' ', '_') + '.txt'

                    with open(os.path.join(folder, filename), 'wb') as file:
                        file.write(body.get_text().strip().encode('utf-8'))

                    print(f"Article '{title}' saved as {filename}")

def main():
    n_pages = int(input("Enter number of pages: "))
    articles_type = input("Enter type of articles: ")

    for i in range(1, n_pages + 1):
        folder_name = f"Page_{i}"
        if i == 1:
            url = f"https://www.nature.com/nature/articles?year=2020"
        else:
            url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={i}"

        stage_4(url, articles_type, folder_name)

    print("Saved all articles.")

if __name__ == "__main__":
    main()

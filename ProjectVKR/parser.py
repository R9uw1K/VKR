import time
import random
import requests
import bs4 as bs
import sqlite3
import json


class Article:
    def __init__(self, name=None, author=None, collection=None, realese=None, pages=None,
                 language=None, path=None, keywords=None, annotation=None, issn=None, science=None):
        self.name, self.author, self.collection, self.realese, self.pages, self.language, self.path, self.keywords, self.annotation, self.issn, self.science = name, author, collection, realese, pages, language,path, keywords, annotation, issn, science

    def add_to_bd(self):
        db = sqlite3.connect('mysite/db.sqlite3')
        cursor = db.cursor()
        insert = '''INSERT INTO articles_article(article_name, article_author, article_collection, article_release, article_pages, article_language, article_path, article_keywords, article_annotation, article_issn, article_science) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        cursor.execute(insert, (self.name, self.author, self.collection, self.realese, self.pages, self.language, self.path, json.dumps(self.keywords), self.annotation, self.issn, self.science))
        db.commit()


class Parser:
    def __init__(self):
        self.session = requests.Session()

    def get_all_articles(self):
        r = self.session.get('http://lobachevskii-dml.ru/journal/kuktf/715')
        info = bs.BeautifulSoup(r.content, 'lxml')
        all_articles = info.find_all(class_='articleItem')
        self.links = []
        for article in all_articles:
            self.links.append(f"http:{article.find('a').get('href')}")
        return self.links

    def get_info_from_article(self):
        for link in self.links:
            try:
                time.sleep(random.randint(1, 5))
                r = self.session.get(link)
                info = bs.BeautifulSoup(r.content, 'lxml')
                base_info = info.find(class_='col-xs-12').find('div').find_all('div')
                name = info.find(id='title').text
                author = info.find(id='authors').text.replace('\n', '')
                realese = info.find(id='volume').text.replace('\n', '')
                collection = base_info[-3].text
                issn = None
                pages = None
                language = None
                annotation = None
                keywords = json.dumps({"0": []})
                science = None
                pdf_link = None
                i = 0
                for item in base_info:
                    if 'ISSN' in item.text:
                        issn = item.text
                    elif 'С.:' in item.text:
                        pages = item.text
                    elif 'Язык' in item.text:
                        language = item.text.split(': ')[1]

                    elif 'Аннотация' in item.text:
                        annotation = item.find('div').text
                    elif 'Ключевые слова' in item.text:
                        keywords = {'0': item.find('div').text.split()}
                    elif 'Научное направление' in item.text:
                        science = item.find('div').text
                    elif item.get('id') == 'volume':
                        collection = base_info[i+1].text
                    elif 'pdf' in str(item).lower():
                        pdf_link = item.find('a').get('href')
                    i += 1
                r = requests.get(pdf_link)
                with open(f'mysite/articles/static/articles/pdf/{realese}-{pages.replace(".", "").replace(":", "")}.pdf', 'wb') as f:
                    f.write(r.content)
                article = Article(name, author, collection, realese, pages, language, f'{realese}-{pages.replace(".", "").replace(":", "")}.pdf', keywords, annotation, issn, science)
                article.add_to_bd()
            except Exception:
                pass



def main():
    p = Parser()
    print(p.get_all_articles())
    p.get_info_from_article()


if __name__ == '__main__':
    main()

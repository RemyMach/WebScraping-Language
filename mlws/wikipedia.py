import requests
from bs4 import BeautifulSoup

class Wikipedia:
    '''
    Class executant une recherche sur Wikipedia

    Return
        Text de la premiere page trouvee
        None si aucun article est trouve
    '''

    def wikiScrape(self, term):
        term = term.replace(' ', '_')

        url = "https://en.wikipedia.org/wiki/%s" % term
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")

        heading = soup.find(id="firstHeading")
        content = soup.find(class_="mw-parser-output")

        result = heading.text + '\n'

        content.find('div', class_="reflist").decompose()
        for elem in content.find_all('div', role="navigation"):
            elem.decompose()

        info = content.find_all(['h3', 'h2', 'p', 'li'])

        for element in info:
            result += element.text + '\n'

        return result
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Google:
    '''
    Class permettant de faire une recherche Google des termes passer

    Return
        Titre et lien du resultat de recherche
        None si la recherche echoue
    '''

    def googleScrape(self, term):
        term = term.replace(' ', '+')

        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)

        url = "https://www.google.com/search?q=%s" % term
        driver.get(url)

        driver.implicitly_wait(1)

        output = driver.find_elements_by_class_name("yuRUbf")

        if len(output) == 0:
            driver.quit()
            return None

        result = ""

        for out in output:
            title = out.find_element_by_tag_name('h3')
            link = out.find_element_by_tag_name('a')

            result += title.text + '||' + link.get_attribute('href') + '\n'
            
        driver.quit()
        return result

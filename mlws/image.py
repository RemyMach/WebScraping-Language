import os, time
from urllib.request import urlretrieve

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Image:
    '''
    Class permettant de recuperer les 10 premieres images de Google image et les sauvegarde dans un dossier

    Return
        True si les images sont sauvegarder
        None si la recherche echoue
    '''

    def imageScrape(self, term, var):
        term = term.replace(' ', '+')

        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)

        url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q=%s&oq=%s&gs_l=img" % (term, term)
        driver.get(url)

        driver.implicitly_wait(1)

        images = driver.find_elements_by_class_name('rg_i')[0:10]

        if len(images) == 0:
            driver.quit()
            return None

        count = 0
        if not os.path.isdir(var):
            os.mkdir(var)
        for image in images:
            image.click()
            time.sleep(1)
            element = driver.find_elements_by_class_name('v4dQwb')

            if count == 0:
                big_img = element[0].find_element_by_class_name('n3VNCb')
            else:
                big_img = element[1].find_element_by_class_name('n3VNCb')

            try:
                urlretrieve(big_img.get_attribute("src"), "%s/%s_image%d.jpg" % (var, term, count))
            except:
                print('[WARNING] Image number %d failed when downloading images for search term: %s' % (count, term))
            count += 1

        driver.quit()
        return True
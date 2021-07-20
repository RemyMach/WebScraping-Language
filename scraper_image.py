from selenium import webdriver  # For dynamic web scraping
from selenium.webdriver.chrome.options import Options   # To add headless option (scrape without a chrome window)
import os, time
from urllib.request import urlretrieve # To save the scraped images

class ScraperImage:
    
    @staticmethod
    def imageScrape(term, var):
        """
            Récupérer les 1à premières images de la recherche google et les sauvegarder dans un bon directory

            Returns
                True si toutes les images sont bien scrap
                None si toutes les images sont pas bien scrap
        """

        # Replace each space with + character
        term = term.replace(' ', '+')

        # Create selenium web driver
        options = Options()
        options.add_argument("--headless") # Run the webdriver without opening a browser window
        driver = webdriver.Chrome(options=options)

        url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q=%s&oq=%s&gs_l=img" % (term, term)
        driver.get(url)

        driver.implicitly_wait(1)

        imgs = driver.find_elements_by_class_name('rg_i')[0:10] # Get first 10 images
        print(imgs)
        if len(imgs) == 0:
            driver.quit() # Quit the driver
            return None

        count = 0
        var = "static/" + var
        if not os.path.isdir(var):
            # If directory doesn't exist, create it
            os.mkdir(var)
        for img in imgs:
            try:
                img.click() # Click the image to get full resolution
            except:
                driver.quit()  # Quit the driver
                return True
            time.sleep(1)
            element = driver.find_elements_by_class_name('v4dQwb')

            # Fetch the image, if condition for google's logic
            if count == 0:
                big_img = element[0].find_element_by_class_name('n3VNCb')
            else:
                big_img = element[1].find_element_by_class_name('n3VNCb')

            #If image is fetched correctly, download it and save it in a file
            try:
                urlretrieve(big_img.get_attribute("src"), "%s/%s_image%d.jpg" % (var, term, count))
            except:
                # An error in the link happened
                print('[WARNING] Image number %d failed when downloading images for search term: %s' % (count, term))
            count += 1

        driver.quit() # Quit the driver
        return True
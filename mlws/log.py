from datetime import datetime
import os

class Log:
    '''
    Class permettant de garder un journal d'execution
    '''
    def __init__(self, directoryName):
        self.directoryName = directoryName

    def execute(self, result, search_type, word):
        if not os.path.isdir(self.directoryName):
            # If directory doesn't exist, create it
            os.mkdir(self.directoryName)
        with open(self.directoryName + "/log.txt", 'a') as f:
            date = str(datetime.now()).replace(' ', '_').split('.')[0]
            if result:
                f.write("%s - searched %s \"%s\" and found something\n" % (date, search_type, word))
            else:
                f.write("%s - searched %s \"%s\" and found nothing\n" % (date, search_type, word))
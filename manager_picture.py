import os
from picture import Picture

class ManagerPicture:
    def __init__(self, pictures: list) -> None:
        self.pictures = pictures

    def addPicture(self, picture) -> None:
        self.pictures.append(picture)

    def setPicturesFromADirectory(self, name):
        if os.path.isdir("static/" + name):
            files = [f for f in os.listdir("static/" + name) if os.path.isfile(os.path.join("static/" + name, f))]
            for file in files:
                self.addPicture(Picture(name + "/" + file))

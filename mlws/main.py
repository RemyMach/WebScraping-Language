import sys

from mlws import MLWS

if __name__ == "__main__":
    filename = sys.argv[1]
    if filename[-5:] == ".mlws":
        mlws = MLWS(filename)
        
        if mlws.validate():
            mlws.parse()
        else:
            print("Error: File not recognized")
    else:
        print("Error: File not recognized")
import sys
from datetime import datetime

from mlws.wikipedia import Wikipedia
from mlws.image import Image
from mlws.google import Google
from mlws.log import Log
import os

class MLWS:
    '''
    Class traitant les operations sur les fichiers .MLWS
    '''

    def __init__(self, fileContent, directoryName):
        try:
            self.directoryName = "results/" + directoryName
            self.textOut = []
            self.data = []
            for line in fileContent.split('\n'):
                self.data.append(line.strip())
                self.currentLine = 0
                self.variables = {}
        except FileNotFoundError:
            print("Error: File not recognized")
            sys.exit(0)

    def validate(self):
        '''
        Validation du fichier et check de la version du code

        Return
            True si le fichier est valid
            False si le fichier est invalid (version superieur q 1.0)
        '''
        first = None
        dataCopy = list(self.data)
        print(self.data)
        for line in dataCopy:
            if line != '':
                first = line
                self.currentLine += 1
                self.data.remove(line)
                break
            self.currentLine += 1
            self.data.remove(line)

        if not first:
            return False
        
        if first[0:6] == "MLWS:v":
            version = float(first.replace("MLWS:v", ''))
        
            if version <= 1:
                return True
            else:
                return False

        else:
            return False

    def out(self, string):
        '''
        Affiche du text dans la console
        '''
        print(string)
        self.textOut.append(string)

    def parse(self):
        '''
        Parse le fichier et execute les instructions
        '''
        if_flag = True
        block_count = 0
        for line in self.data:
            self.currentLine += 1
            instruction = line.split('!')[0]
            if instruction == '':
                continue
            
            command = instruction.split(' ')[0]
            
            if command == 'out':
                if if_flag:
                    text = instruction.replace(command, '')
                    output = ""
                    index = 0
                    for char in text:
                        if char == '"':
                            index += 1
                            break
                        elif char == ' ':
                            index += 1
                        else:
                            print("[line %d] Syntax Error: Invalid character at position {%d}: %s" % (self.currentLine, index, char))
                            sys.exit(0)

                    char = text[index]
                    while char != '"':
                        output += char
                        index += 1
                        if index == len(text):
                            print("[line %d] EOF Error: Unexpected end of file (missing \"?)" % (self.currentLine))
                            sys.exit(0)
                        char = text[index]
                    
                    index += 1
                    while index < len(text):
                        if text[index] != ' ':
                            print("[line %d] Syntax Error: Invalid character at position {%d}: %s" % (self.currentLine, index, text[index]))
                            sys.exit(0)
                        index += 1

                    print(output)
                    self.textOut.append(output)

            elif command == 'search':
                if if_flag:
                    text = instruction.replace(command, '')
                    word = ""
                    index = 0
                    for char in text:
                        if char == '"':
                            index += 1
                            break
                        elif char == ' ':
                            index += 1
                        else:
                            print("[line %d] Syntax Error: Invalid character at position {%d}: %s" % (self.currentLine, index, char))
                            sys.exit(0)

                    char = text[index]
                    while char != '"':
                        word += char
                        index += 1
                        if index == len(text):
                            print("[line %d] EOF Error: Unexpected end of file (missing \"?)" % (self.currentLine))
                            sys.exit(0)
                        char = text[index]
                    
                    index += 1
                    rest = text[index:].split(' ')

                    var = None
                    options = []

                    for item in rest:
                        if not item:
                            continue
                        if item[0] != '-':
                            if not var:
                                var = item
                            else:
                                print("[line %d] Syntax Error: Invalid variable name at position {%d}" % (self.currentLine, index))
                                sys.exit(0)
                        else:
                            if item not in ['-i', '-w', '-l']:
                                print("[line %d] Syntax Error: Invalid option at position {%d}" % (self.currentLine, index))
                                sys.exit(0)
                            else:
                                options.append(item)
                    
                    if '-i' in options and '-w' in options:
                        print("[line %d] Logic Error: Can't use both options [-i] and [-w]" % self.currentLine)
                        sys.exit(0)

                    search_type = ""
                    if '-w' in options:
                        wikipedia = Wikipedia()
                        result = wikipedia.wikiScrape(word)
                        self.variables[var] = result
                        search_type = "on wikipedia"
                    elif '-i' in options:
                        image = Image()
                        result = image.imageScrape(word, var)
                        search_type = "image"
                    else:
                        google = Google()
                        result = google.googleScrape(word)
                        self.variables[var] = result

                    if '-l' in options:
                        log = Log(self.directoryName)
                        log.execute(result, search_type, word)

            elif command == 'save':
                if if_flag:
                    args = instruction.split(' ')
                    if len(args) != 3:
                        print("[line %d] Syntax Error: Invalid number of arguments: expected 3, got %d" % (self.currentLine, len(args)))
                        sys.exit(0)
                    
                    if args[1] not in self.variables.keys():
                        print("[line %d] Syntax Error: Variable doesn't exist: %s" % (self.currentLine, args[1]))
                        sys.exit(0)
                    
                    result = self.variables[args[1]]
                    if not os.path.isdir(self.directoryName):
                        # If directory doesn't exist, create it
                        os.mkdir(self.directoryName)
                    with open(self.directoryName + "/" +args[2], 'w') as f:
                        f.write(result)

            elif command == 'if':
                args = instruction.split(' ')
                if len(args) != 4:
                    print("[line %d] Syntax Error: Invalid number of arguments: expected 4, got %d" % (self.currentLine, len(args)))
                    sys.exit(0)

                block_count += 1

                var1 = args[1]
                var2 = args[3]

                if var1 not in self.variables.keys():
                    print("[line %d] Value Error: Variable doesn't exist: %s" % (self.currentLine, var1))
                    sys.exit(0)
                var1 = self.variables[var1]

                if var2 == "null":
                    var2 = None
                else:
                    if var2 not in self.variables.keys():
                        print("[line %d] Value Error: Variable doesn't exist: %s" % (self.currentLine, var2))
                        sys.exit(0)
                    var2 = self.variables[var2]
                
                condition = args[2]
                if condition == 'is':
                    if var1 == var2:
                        if_flag = True
                    else:
                        if_flag = False

                elif condition == "isnt":
                    if var1 != var2:
                        if_flag = True
                    else:
                        if_flag = False
            
            elif command == "else":
                args = instruction.split(' ')
                if len(args) != 1:
                    print("[line %d] Syntax Error: Invalid number of arguments: expected 1, got %d" % (self.currentLine, len(args)))
                    sys.exit(0)

                if block_count <= 0:
                    print("[line %d] Syntax Error: Expected 'if' before 'else' statement" % self.currentLine)
                    sys.exit(0)
                
                if_flag = not if_flag
            
            elif command == "done":
                args = instruction.split(' ')
                if len(args) != 1:
                    print("[line %d] Syntax Error: Invalid number of arguments: expected 1, got %d" % (self.currentLine, len(args)))
                    sys.exit(0)
                
                if block_count <= 0:
                    print("[line %d] Syntax Error: Expected 'if' before 'done' statement" % self.currentLine)
                    sys.exit(0)
                
                if_flag = True
                block_count -= 1
            
            else:
                print("[line %d] Syntax Error: Unknown command {%s}" % (self.currentLine, command))
                sys.exit(0)

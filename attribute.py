import numpy as np

class Attribute(object):

    def __init__(self, attributeName, types):
        if isinstance(types, list) == True:
            self.types = types
        else:
            self.types = [types]
        self.name = attributeName.replace("'","")
        self.cases = []

    def areCasesValid(self):
        for case in range(len(self.cases)):
            testVar = False
            if self.types[0] == "STRING":
                if isinstance(self.cases[case], str) == True:
                    testVar = True
            elif self.types[0] == "numeric":
                if isinstance(self.cases[case], float) == True:
                    testVar = True
                else:
                    try:
                        self.cases[case] = float(self.cases[case])
                        testVar = True
                    except:
                        if self.cases[case] == "?":
                            testVar = True
                        else:
                            print(self.cases[case])
                            print("num")
                            print(self.name)
                            return False
            else:
                for type in self.types:
                    if self.cases[case] == type or self.cases[case] == "?":
                        testVar = True
            if testVar == False:
                print(self.cases[case])
                print(self.name)
                print(self.types)
                return False
        return True

    def getTypeIndex(self,compare):
        for type in range(len(self.types)):
            if compare == self.types[type]:
                return type

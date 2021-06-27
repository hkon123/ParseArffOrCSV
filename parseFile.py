import numpy as np
from attribute import Attribute
import re

class ParseFile(object):

    def parseFilefromKeywords(file, keyword1, keyword2):
        param1 = []
        param2 = []
        f = open(file)
        firstLine = 0
        for line in f:
            if firstLine == 0:
                header = line.split(chr(9))
                headerCount = 0
                for words in header:
                    if words.rstrip("\n") == keyword1:
                        keyword1Counter = headerCount
                        headerCount+=1
                    elif words.rstrip("\n") == keyword2:
                        keyword2Counter = headerCount
                        headerCount+=1
                    else:
                        headerCount+=1
                firstLine = 1
                continue
            else:
                wordCount = 0
                words = line.split(chr(9))
                for word in words:
                    if wordCount == keyword1Counter:
                        try:
                            param1.append(float(word)) #store total_income
                        except:
                            param1.append(-1.0)
                        wordCount+=1
                    elif wordCount == keyword2Counter:
                        try:
                            param2.append(float(word))#store loan_amount
                        except:
                            param2.append(-1.0)
                        wordCount+=1
                    else:
                        wordCount+=1
        return param1, param2


    def parseFileFromOneKeyword(file, keyword1):
        param1 = []
        f = open(file)
        firstLine = 0
        for line in f:
            if firstLine == 0:
                header = line.split(chr(9))
                headerCount = 0
                for words in header:
                    if words.rstrip("\n") == keyword1:
                        keyword1Counter = headerCount
                        headerCount+=1
                    else:
                        headerCount+=1
                firstLine = 1
                continue
            else:
                wordCount = 0
                words = line.split(chr(9))
                for word in words:
                    if wordCount == keyword1Counter:
                        try:
                            param1.append(float(word)) #store total_income
                        except:
                            param1.append(-1.0)
                        wordCount+=1
                    else:
                        wordCount+=1
        return param1


    def parseArffFile(file):
        f = open(file)
        attributes = []
        dataFlag = False
        for line in f:
            reducedLine = line.split(" ")
            if dataFlag == True:
                caseLine = line.split(",")
                for i in range(len(caseLine)):
                    attributes[i].cases.append(caseLine[i].rstrip("\n").strip("/'").lstrip(" '"))
            elif reducedLine[0] == "@attribute":
                if reducedLine[2].rstrip("\n") == "STRING":
                    attributes.append(Attribute(reducedLine[1], reducedLine[2].rstrip("\n")))
                    continue
                if reducedLine[2].rstrip("\n") == "numeric":
                    attributes.append(Attribute(reducedLine[1], reducedLine[2].rstrip("\n")))
                    continue
                subLine = line.split("{")
                subSubLine = subLine[1].split("}")
                subSubSubLine = subSubLine[0].split(",")
                attributes.append(Attribute(reducedLine[1], ParseFile.stripArray(subSubSubLine)))
            elif reducedLine[0].rstrip("\n") == "@data":
                dataFlag = True
                continue
            else:
                continue
        for attribute in attributes:
            if attribute.areCasesValid()!=True:
                print("ERROR in parsing, check input file!")
                ParseFile.printArffFile(attributes)
                return None
        return attributes



    def parseCSVFile(file):
        f = open(file)
        attributes = []
        dataFlag = False
        for line in f:
            #print(dataFlag)
            if dataFlag == True:
                #reducedLine = line.split(",")

                regLine = re.findall("(?:,|\n|^)(\"(?:(?:"")*[^\"]*)*\"|[^\",\n]*|(?:\n|$))", line)#"(,(?=\S)|:)", line)
                #print(len(regLine))
                count = 0
                for i in range(len(regLine)):
                    if regLine[i] == ',':
                        continue
                    else:
                        if count < len(attributes):
                            attributes[count].cases.append(regLine[i].rstrip("\n").strip("\"").lstrip("\""))
                            count+=1
                            #print(regLine[i])
                            #print(count)
                continue
            else:
                reducedLine = line.split(",")
                print(len(reducedLine))
                for attr in reducedLine:
                    attributes.append(Attribute(attr.rstrip("\n").strip("\"").lstrip("\""), "STRING"))
                dataFlag = True
                continue

            '''
        for attribute in attributes:
            if attribute.areCasesValid()!=True:
                print("ERROR in parsing, check input file!")
                ParseFile.printArffFile(attributes)
                return None
                '''
        return attributes



    def printArffFile(attributes):
        for attribute in attributes:
            print(attribute.name, end= " | " + chr(9))
            if len(attribute.name) < 5:
                print(chr(9), end = "")
        print("\n")
        for case in range(len(attributes[1].cases)):
            for attribute in attributes:
                print(attribute.cases[case], end = " | " )
                try:
                    if len(attribute.cases[case]) < 5:
                        print(3*chr(9), end = "")
                    elif len(attribute.cases[case]) < 13:
                        print(2*chr(9), end = "")
                    elif len(attribute.cases[case]) < 21:
                        print(chr(9), end = "")
                except:
                    print(3*chr(9), end = "")
            print("")

    def replaceMissingValues(attributes, replacement):
        for case in range(len(attributes[1].cases)):
            for attribute in attributes:
                if len(attribute.cases[case]) == 0:
                    attribute.cases[case] = replacement
        return attributes

    def replaceValueInAttribute(attributes, attributeName, value, replacement):
        for attribute in attributes:
            if attribute.name == attributeName:
                for case in range(len(attribute.cases)):
                    if attribute.cases[case] == value:
                        attribute.cases[case] = replacement
        return attributes

    def stripArray(array):
        for i in range(len(array)):
            array[i] = array[i].replace("'","")#rstrip("'").lstrip(" '")
            array[i] = array[i].replace(" ","")
        return array

    def getMeanFromAttribute(attributes, attributeName):
        for attribute in attributes:
            if attribute.name == attributeName:
                if attribute.types[0]!= "numeric":
                    return none
                else:
                    count = 0
                    sum = 0
                    for case in attribute.cases:
                        if case != "?":
                            sum+=case
                            count+=1
        return sum/count

    def arrfAttributesToFile(file, attributes, relation):
        file.write("@relation " + ParseFile.setStringWrapper(relation) + "\n\n")
        for attribute in attributes:
            if attribute.types[0] == "STRING" or attribute.types[0] == "numeric":
                    file.write("@attribute " + ParseFile.setStringWrapper(attribute.name) + " " + attribute.types[0] + "\n")
            else:
                    file.write("@attribute " + ParseFile.setStringWrapper(attribute.name) + " {")
                    for type in attribute.types:
                        file.write(ParseFile.setStringWrapper(type))
                        if type!= attribute.types[-1]:
                            file.write(",")
                    file.write("}\n")
        file.write("\n@data\n")
        for case in range(len(attributes[0].cases)):
            for attribute in attributes:
                file.write(ParseFile.setStringWrapper(attribute.cases[case]))
                if attribute!= attributes[-1]:
                    file.write(",")
            file.write("\n")


    def setStringWrapper(string):
        try:
            if len(string.split()) > 1:
                return "\"" + string + "\""
            else:
                return string
        except:
            return str(string)


    def getAttribute(data, attrName):
        for attribute in data:
            if attribute.name == attrName:
                return attribute
        return Attribute("None in data", "STRING")

    def setAttributeTypes(attribute):
        types = [0]
        for case in attribute.cases:
            typeFlag = True
            for type in types:
                if case == type:
                    typeFlag = False
            if typeFlag == True:
                types.append(case)
        attribute.types = types[1:]

    def getDataSubset(data,attrNames):
        subset = []
        for name in attrNames:
            subset.append(ParseFile.getAttribute(data,name))
            ParseFile.setAttributeTypes(subset[-1])
        return subset

    def removeCasesFromData(data,removeType):
        for attr in range(len(data)):
            case = 0
            while case < len(data[attr].cases):
                if data[attr].cases[case] == removeType:
                    for subAttr in range(len(data)):
                            del data[subAttr].cases[case]
                else:
                    case +=1
        for attr in data:
            type = 0
            while type < len(attr.types):
                if attr.types[type] == removeType:
                    del attr.types[type]
                else:
                    type+=1

    def removeCasesFromDataAttr(data,removeType,attribute):
        case = 0
        while case < len(attribute.cases):
            if attribute.cases[case] == removeType:
                for subAttr in range(len(data)):
                    del data[subAttr].cases[case]
            else:
                case +=1

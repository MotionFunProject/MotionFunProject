# JSON_parser.py reads a text file and filters


import json
from math import pi


f = open("datalog.txt", "r")
output = open("datalog2.txt", "w")
output.write(f.read().replace("data:", "").replace("", ""))
f.close()
output.close()


def toRadians(angle):
    return angle * pi / 180.0


def getCordinates():
    output = open("cor.txt", "w")
    with open("datalog2.txt") as file:
        listCor = []
        for i in file:

            coordinate = []
            data = json.loads(i)
            coordinate.append(toRadians(data['heading']))
            coordinate.append(toRadians(data['roll']))
            coordinate.append(toRadians(data['pitch']))
            listCor.append(coordinate)
        cor = str(listCor)
        cor = cor.replace("[", "")
        cor = cor.replace("]", "")
        output.write(cor)
        output.close()

getCordinates()




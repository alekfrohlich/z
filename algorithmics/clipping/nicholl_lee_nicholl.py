import numpy as np
import math

# Inside
# add(x1,10,10;20,20)
# add(x2,470,470;480,520)
# add(x3,400,400;600,400)
# add(x4,50,50;25,-100)
# add(x5,100,100;-100,40)

# West
# add(x7,-50,250;250,260)
# add(x8,-50,250;250,600)
# add(x9,-50,250;250,-100)
# add(x10,-50,250;600,260)
# add(x11,-50,250;-60,260)
# add(x12,-500,250;250,3000)

# North
# add(x7,250,550;260,260)
# add(x88,250,550;600,-1)
# add(x99,250,550;-250,-1)
# add(x10,250,550;200,-260)
# add(x11,250,550;260,560)
# add(x12,400,1050;6050,500)

# NE
# add(x15,750,850;400,-50)
# NW
# add(x16,-250,850;400,-50)
# add(x17,-250,850;600,400)
# add(x19,-250,850;50,-50)
# add(x18,-250,850;-300,900)

# y1 = x1*m + b
# y2 = x2*m + b
# y1-y2 = m*(x1-x2)
# m = (y1-y2)/(x1-x2)

# M's code
# 0---------1
# |         |
# |         |
# |         |
# 3---------2


def nln(points):

    x1, y1, _ = points[0]
    x2, y2, _ = points[1]
    new_points = 0
    npo = [np.array([0., 0., 1.]), np.array([0., 0., 1.])]

    def pos(x,y):
        pos = ""
        if y > 1:
            pos += "N"
        elif y < -1:
            pos += "S"
        if x > 1:
            pos += "E"
        elif x < -1:
            pos += "W"
        if pos == "":
            pos += "I"
        return pos

    pos1 = pos(x1,y1)
    pos2 = pos(x2,y2)
    m = []
    ml = 0
    function = True
    if x1-x2 == 0:
        function = False
    if function:
        ml = (y1-y2)/(x1-x2)
    valid = False

    def calculateMs():
        # precisa tratar casos em que p1 ta embaixo ou em cima de uma das bordas? SIMMMMMMM!!!!!!! (quando eh funcao)
        # dar valor de m grande eh uma solucao? nos testes o algoritmo funcionou (continua sem solucao)

        m.append((y1-1)/(x1+1))
        m.append((y1-1)/(x1-1))
        m.append((y1+1)/(x1-1))
        m.append((y1+1)/(x1+1))


    def intersectNorth():
        nonlocal new_points, valid, npo
        npo[new_points][0] = (1 - y1 + ml*x1) / ml
        npo[new_points][1] = 1
        new_points+=1
        valid = True
        # print(npo)
        print("north")

    def intersectSouth():
        nonlocal new_points, valid, npo
        npo[new_points][0] = (-1-y1+ml*x1)/ml
        npo[new_points][1] = -1
        new_points+=1
        valid = True
        # print(npo)
        print("south")

    def intersectWest():
        nonlocal new_points, valid, npo
        npo[new_points][1] = ml*(-1-x1) + y1
        npo[new_points][0] = -1
        new_points+=1
        valid = True
        # print(npo)
        print("west")

    def intersectEast():
        nonlocal new_points, valid, npo
        npo[new_points][1] = ml*(1-x1) + y1
        npo[new_points][0] = 1
        new_points+=1
        valid = True
        # print(npo)
        print("east")

    def intersectNorthNotFunction():
        nonlocal new_points, valid, npo
        npo[new_points][0] = x1
        npo[new_points][1] = 1
        new_points+=1
        valid = True
        # print(npo)
        print("northSpe")

    def intersectSouthNotFunction():
        nonlocal new_points, valid, npo
        npo[new_points][0] = x1
        npo[new_points][1] = -1
        new_points+=1
        valid = True
        # print(npo)
        print("southSpe")

    def inside():
        nonlocal valid
        print("inside")
        if pos2 == "I":
            print("doubleinside")
            valid = True
        elif not function:
            if  pos2 == "N":
                print("nnnnnnnn")
                intersectNorthNotFunction()
            elif pos2 == "S":
                print("sssssssss")
                intersectSouthNotFunction()
            else:
                print("EEEEEEErro")
        else:
            calculateMs()
            # north
            if   abs(ml) > abs(m[0]) and abs(ml) >= m[1] and y2 > y1:
                intersectNorth()
            # east
            elif ml < m[1] and ml >= m[2] and x2 > x1:
                intersectEast()
            # south
            elif abs(ml) > abs(m[2]) and abs(ml) >= m[3] and y2 < y1:
                intersectSouth()
            # west
            elif ml < m[3] and ml >= m[0] and x2 < x1:
                intersectWest()
            else:
                print("error")

    def side():
        if function:
            calculateMs()
        if pos1 in pos2:
            print("impossivel")
            return
            # print("same side")

        elif pos1 == "W":
            if ml < m[0] and ml > m[1]:
                intersectWest()
                if "N" in pos2:
                    intersectNorth()
            elif ml <= m[1] and ml >= m[2]:
                intersectWest()
                if pos2 != "I":
                    intersectEast()
            elif ml < m[2] and ml > m[3]:
                intersectWest()
                if "S" in pos2:
                    intersectSouth()

        elif pos1 == "N":
            if function:
                if ml < m[1] and ml > m[2]:
                    intersectNorth()
                    if "E" in pos2:
                        intersectEast()
                elif ml <= m[2] or ml >= m[3]:
                    intersectNorth()
                    if pos2 != "I":
                        intersectSouth()
                elif ml > m[0] and ml < m[3]:
                    intersectNorth()
                    if "W" in pos2:
                        intersectWest()
            else:
                print("descobrir se intersecta north and south")
                if  pos2 == "I":
                    print("iiiiiiii")
                    intersectNorthNotFunction()
                elif pos2 == "S":
                    print("ssssssss")
                    intersectNorthNotFunction()
                    intersectSouthNotFunction()
                else:
                    print("Errrrrro")

        elif pos1 == "E":
            if ml < m[2] and ml > m[3]:
                intersectEast()
                if "S" in pos2:
                    intersectSouth()
            elif ml <= m[3] and ml >= m[0]:
                intersectEast()
                if pos2 != "I":
                    intersectWest()
            elif ml < m[0] and ml > m[1]:
                intersectEast()
                if "N" in pos2:
                    intersectNorth()

        elif pos1 == "S":
            if function:
                if ml < m[3] and ml > m[0]:
                    intersectSouth()
                    if "W" in pos2:
                        intersectWest()
                elif ml <= m[0] or ml >= m[1]:
                    intersectSouth()
                    if pos2 != "I":
                        intersectNorth()
                elif ml < m[1] and ml > m[2]:
                    intersectSouth()
                    if "E" in pos2:
                        intersectEast()
            else:
                print("descobrir se intersecta north and south")
                if  pos2 == "I":
                    print("iiiiiiii")
                    intersectSouthNotFunction()
                elif pos2 == "N":
                    print("nnnnnnnnn")
                    intersectNorthNotFunction()
                    intersectSouthNotFunction()
                else:
                    print("Errrrrro")

        if new_points == 0:
            print("out")

    def diagonal():
        print("diagonal")
        calculateMs()
        if pos1 == "NW":
            if "N" in pos2 or "W" in pos2:
                # it's necessary to return otherwise it might consider the reflection of p2
                return
                # print("out")
            if m[0] < m[2]:
                first = 2
                second = 0
            else:
                first = 0
                second = 2
            if ml < m[1] and ml >= m[first]:
                intersectNorth()
                if "E" in pos2:
                    intersectEast()
            elif ml < m[first] and ml >= m[second]:
                if m[0] < m[2]:
                    intersectNorth()
                    if "S" in pos2:
                        intersectSouth()
                else:
                    intersectWest()
                    if "E" in pos2:
                        intersectEast()
            elif ml < m[second] and ml >= m[3]:
                intersectWest()
                if "S" in pos2:
                    intersectSouth()

        if pos1 == "SE":
            if "S" in pos2 or "E" in pos2:
                return
                # print("out")
            if m[0] > m[2]:
                first = 2
                second = 0
            else:
                first = 0
                second = 2
            if ml > m[1] and ml <= m[first]:
                intersectEast()
                if "N" in pos2:
                    intersectNorth()
            elif ml > m[first] and ml <= m[second]:
                if m[0] > m[2]:
                    intersectSouth()
                    if "N" in pos2:
                        intersectNorth()
                else:
                    intersectEast()
                    if "W" in pos2:
                        intersectWest()
            elif ml > m[second] and ml <= m[3]:
                intersectSouth()
                if "W" in pos2:
                    intersectWest()

        if pos1 == "SW":
            if "S" in pos2 or "W" in pos2:
                return
                # print("out")
            if m[1] > m[3]:
                first = 1
                second = 3
            else:
                first = 3
                second = 1
            if ml < m[0] and ml >= m[first]:
                intersectWest()
                if "N" in pos2:
                    intersectNorth()
            elif ml < m[first] and ml >= m[second]:
                if m[1] > m[3]:
                    intersectWest()
                    if "W" in pos2:
                        intersectEast()
                else:
                    intersectSouth()
                    if "N" in pos2:
                        intersectNorth()
            elif ml < m[second] and ml >= m[2]:
                intersectSouth()
                if "E" in pos2:
                    intersectEast()


        if pos1 == "NE":
            if "N" in pos2 or "E" in pos2:
                return
                # print("out")
            if m[1] < m[3]:
                first = 1
                second = 3
            else:
                first = 3
                second = 1
            if ml > m[0] and ml <= m[first]:
                intersectNorth()
                if "W" in pos2:
                    intersectWest()
            elif ml > m[first] and ml <= m[second]:
                if m[1] < m[3]:
                    intersectEast()
                    if "W" in pos2:
                        intersectWest()
                else:
                    intersectNorth()
                    if "S" in pos2:
                        intersectSouth()
            elif ml > m[second] and ml <= m[2]:
                intersectEast()
                if "S" in pos2:
                    intersectSouth()

        if new_points == 0:
            pass
            # print("out")

    print(pos1)
    if pos1 == "I":
        inside()
    elif len(pos1) == 1:
        side()
    else:
        diagonal()

    if not valid:
        return None
    if   new_points == 0:
        npo[0] = points[0]
        npo[1] = points[1]
    elif new_points == 1:
        if pos1 == "I":
            npo[1] = points[0]
        else:
            npo[1] = points[1]
    elif new_points == 2:
        pass
    else:
        print("errorrrr")

    print(npo)
    return (npo[0], npo[1])


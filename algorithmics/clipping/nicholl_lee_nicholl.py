import numpy as np

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

    x1, y1, _ = points[0]
    x2, y2, _ = points[1]
    pos1 = pos(x1,y1)
    pos2 = pos(x2,y2)
    m = []
    ml = (y1-y2)/(x1-x2)
    intersected = False

    def calculateMs():
        m.append((y1-1)/(x1+1))
        m.append((y1-1)/(x1-1))
        m.append((y1+1)/(x1-1))
        m.append((y1+1)/(x1+1))

    def inside():
        print("inside")
        if pos2 == "I":
            print("doubleinside")
            return
        else:
            calculateMs()
            # north
            if   abs(ml) > abs(m[0]) and abs(ml) >= m[1] and y2 > y1:
                print("north")
            # east
            elif ml < m[1] and ml >= m[2] and x2 > x1:
                print("east")
            # south
            elif abs(ml) > abs(m[2]) and abs(ml) >= m[3] and y2 < y1:
                print("south")
            # west
            elif ml < m[3] and ml >= m[0] and x2 < x1:
                print("west")
            else:
                print("error")

    def side():
        calculateMs()
        if pos1 in pos2:
            print("same side")
            points = None
            return

        elif pos1 == "W":
            if ml < m[0] and ml > m[1]:
                print("west")
                print("north")
            elif ml <= m[1] and ml >= m[2]:
                print("west")
                if pos2 != "I":
                    print("east")
            elif ml < m[2] and ml > m[3]:
                print("west")
                print("south")

        elif pos1 == "N":
            if ml < m[1] and ml > m[2]:
                print("north")
                print("east")
            elif abs(ml) >= m[2] and abs(ml) >= m[3]:
                print("north")
                if pos2 != "I":
                    print("south")
            elif ml > m[0] and ml < m[3]:
                print("north")
                print("west")

        elif pos1 == "E":
            if ml < m[2] and ml > m[3]:
                print("east")
                print("south")
            elif abs(ml) <=m[3] and abs(ml) <= abs(m[0]):
                print("east")
                if pos2 != "I":
                    print("west")
            elif ml < m[0] and ml > m[1]:
                print("east")
                print("north")

        elif pos1 == "S":
            if ml < m[3] and ml > m[0]:
                print("south")
                print("west")
            elif abs(ml) >= abs(m[0]) and abs(ml) >= m[1]:
                print("south")
                if pos2 != "I":
                    print("north")
            elif ml < m[1] and ml > m[2]:
                print("south")
                print("east")

        if not intersected:
            print("out")
            points = None

    def diagonal():
        print("diagonal")
        calculateMs()
        if pos1 == "NW":
            if "N" in pos2 or "W" in pos2:
                print("out")
            if m[0] < m[2]:
                first = 2
                second = 0
            else:
                first = 0
                second = 2
            if ml < m[1] and ml >= m[first]:
                print("north")
                print("east")
            elif ml < m[first] and ml >= m[second]:
                if m[0] < m[2]:
                    print("north")
                    print("south")
                else:
                    print("west")
                    print("east")
            elif ml < m[second] and ml >= m[3]:
                print("west")
                print("south")

        if pos1 == "SE":
            if "S" in pos2 or "E" in pos2:
                print("out")
            if m[0] > m[2]:
                first = 2
                second = 0
            else:
                first = 0
                second = 2
            if ml > m[1] and ml <= m[first]:
                print("north")
                print("east")
            elif ml > m[first] and ml <= m[second]:
                if m[0] > m[2]:
                    print("north")
                    print("south")
                else:
                    print("west")
                    print("east")
            elif ml > m[second] and ml <= m[3]:
                print("west")
                print("south")

        if pos1 == "SW":
            if "S" in pos2 or "W" in pos2:
                print("out")
            if m[1] > m[3]:
                first = 1
                second = 3
            else:
                first = 3
                second = 1
            if ml < m[0] and ml >= m[first]:
                print("west")
                print("north")
            elif ml < m[first] and ml >= m[second]:
                if m[1] > m[3]:
                    print("west")
                    print("east")
                else:
                    print("south")
                    print("north")
            elif ml < m[second] and ml >= m[2]:
                print("south")
                print("east")


        if pos1 == "NE":
            if "N" in pos2 or "E" in pos2:
                print("out")
            if m[1] < m[3]:
                first = 1
                second = 3
            else:
                first = 3
                second = 1
            if ml > m[0] and ml <= m[first]:
                print("west")
                print("north")
            elif ml > m[first] and ml <= m[second]:
                if m[1] < m[3]:
                    print("west")
                    print("east")
                else:
                    print("north")
                    print("south")
            elif ml > m[second] and ml <= m[2]:
                print("south")
                print("east")

        if not intersected:
            print("out")
            points = None
    print(pos1)
    if pos1 == "I":
        inside()
    elif len(pos1) == 1:
        side()
    else:
        diagonal()

    return points

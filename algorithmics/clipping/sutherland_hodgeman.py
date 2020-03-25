import numpy as np

# y = m*x + b
def intersect(p1, p2,xw,yw):
    # print("INTERSECT")
    x1,y1,_ = p1
    x2,y2,_ = p2

    if x1-x2 != 0:
        m = (y1-y2) / (x1-x2)
        b = y1 - m*x1

        # print(m)
        # print(b)

        if yw != None:
            xw = (yw-b)/m
        else:
            yw = m*xw + b
    else:
        if yw != None:
            xw = x1
        else:
            pass
            # print("OOOOOps")

    # print(xw)
    # print(yw)
    return np.array([xw,yw,1])

xw = [-1, None, 1, None]
yw = [None, 1, None, -1]

def sutherHodge(points):

    border = 0

    def out(point):
        if   border == 0:
            return point[0] < -1
        elif border == 1:
            return point[1] > 1
        elif border == 2:
            return point[0] > 1
        else:
            return point[1] < -1

    # print(points)
    # print(type(points))
    old_points = points
    new_points = []

    for _ in range(border, 4):
        # print("BORDER===================")
        # print(border)
        for i in range(len(old_points) - 1):
            if   out(old_points[i]) and out(old_points[i+1]):
                # print("OO")
                pass
            elif (not out(old_points[i])) and out(old_points[i+1]):
                # print("IO")
                new_points.append(intersect(old_points[i], old_points[i+1], xw[border], yw[border]))
            elif out(old_points[i]) and (not out(old_points[i+1])):
                # print("OI")
                new_points.append(intersect(old_points[i], old_points[i+1], xw[border], yw[border]))
                new_points.append(old_points[i+1])
            else:
                # print("II")
                new_points.append(old_points[i+1])
        if len(new_points) != 0:
            new_points.append(new_points[0])
        old_points = new_points[:]
        new_points = []
        border+=1


    # print("POINTS")
    # print(points)
    # print("OLD")
    # print(old_points)
    # print("NEW")
    # print(new_points)

    return old_points
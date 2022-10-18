from random import randint, seed, random
import matplotlib.pyplot as plt
import bintrees
from .classes import Dot, Endpoint


class Segment:
    def __init__(self, left: Dot, right: Dot, label):
        self.left = left
        self.right = right
        self.label = label

    def __repr__(self):
        return f'( {self.left} -> {self.right}, {self.label} )'

    def __eq__(self, other):
        if (self.left == other.left and self.right == other.right and self.label == other.label):
            return True
        return False


def sortDotsByPolarAngle(dotsParam) -> list:
    dots = dotsParam.copy()
    anchor = dots[0]
    indx = 0
    anchor_indx = indx
    # find anchor
    for p in dots:
        if p.y < anchor.y:
            anchor = p
            anchor_indx = indx
        elif (p.y == anchor.y and p.x < anchor.x):
            anchor = p
            anchor_indx = indx
        indx += 1

    # normalize dots
    norm_dots = []
    dots.pop(anchor_indx)
    for dot in dots:
        norm_dots.append(dot - anchor)

    norm_dots.sort()

    sorted_dots = [anchor]
    for dot in norm_dots:
        sorted_dots.append(dot + anchor)

    return sorted_dots


def noise(x) -> float:
    return x + random()


def isLeftTurn(a, b, c) -> bool:
    B = b - a
    C = c - a

    term1 = (B.x)*(C.y)
    term2 = (B.y)*(C.x)
    return (term1 - term2) > 0


def Graham(DotListParam) -> list:
    DotList = DotListParam
    stack = []
    stack.append(DotList[0])
    stack.append(DotList[1])
    stack.append(DotList[2])

    for i in range(3, len(DotList), 1):
        laster = len(stack) - 1
        while not isLeftTurn(stack[laster - 1], stack[laster], DotList[i]):
            stack.pop()
            laster -= 1
        stack.append(DotList[i])

    return stack


# Verifica se o ponto p3 está na semireta p1p2.
# p1, p2 e p3 são colineares
def on_segment(p1: Dot, p2: Dot, p3: Dot):
    p1HasLessX = p1.x < p2.x
    if p1HasLessX and p1.x <= p3.x and p2.x >= p3.x:
        return True
    if p2.x <= p3.x and p1.x >= p3.x:
        return True
    return False


def direction(a, b, c):
    # return 1 if turn left
    # return -1 if turn right
    # return 0 if is co-linear

    B = b - a
    C = c - a

    term1 = (B.x)*(C.y)
    term2 = (B.y)*(C.x)
    return (term1 - term2)


def aux_segments_intersect(p1, p2, p3, p4):
    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    if d1 == 0 and on_segment(p3, p4, p1):
        return True
    if d2 == 0 and on_segment(p3, p4, p2):
        return True
    if d3 == 0 and on_segment(p1, p2, p3):
        return True
    if d4 == 0 and on_segment(p1, p2, p4):
        return True

    return False


def segments_intersect(s1: Segment, s2: Segment):
    return aux_segments_intersect(s1.left, s1.right, s2.left, s2.right)


def isAbove(avl, key):
    if avl.__contains__(key):
        try:
            segment = avl.succ_item(key)[1]
            return (True, segment)
        except:
            return False, 'error'
    else:
        try:
            segment = avl.ceiling_item(key)[1]
            return (True, segment)
        except:
            return False, 'error'


def isBelow(avl, key):
    if avl.__contains__(key):
        try:
            segment = avl.prev_item(key)[1]
            return (True, segment)
        except:
            return False, 'error'
    else:
        try:
            segment = avl.floor_item(key)[1]
            return (True, segment)
        except:
            return False, 'error'


def sweepLineIntersection(endpoitsList, segmentsList):
    avl = [bintrees.AVLTree(), bintrees.AVLTree()]

    for p in endpoitsList:

        s = segmentsList[p.segmentIndx]

        # print(20 * '-')
        # print(avl[0])
        # print(avl[1])
        # print(s, '\t', p.segmentIndx)

        # Insere o segmento na arvore
        if p.endpointType == 'left':

            # Insere o segmento na arvore
            if avl[s.label].__contains__(s.left.y):
                itemList = avl[s.label].get(s.left.y)
                itemList.append(s)
                avl[s.label].insert(s.left.y, itemList)
            else:
                avl[s.label].insert(s.left.y, [s])

            aboveExist, otherSegments = isAbove(avl[s.label - 1], s.left.y)
            if (aboveExist):
                for other in otherSegments:
                    hasIntersection = segments_intersect(s, other)
                    # print("above has Intersect: ", hasIntersection)
                    if (hasIntersection):
                        return True

            belowExist, otherSegments = isBelow(avl[s.label - 1], s.left.y)
            if (belowExist):
                for other in otherSegments:
                    hasIntersection = segments_intersect(s, other)
                    # print("below has Intersect: ", hasIntersection)
                    if (hasIntersection):
                        return True

            # print("isAbove: ", aboveExist, "\t isBelow: ", belowExist)
            # print()

        else:
            aboveExistOther, aboveSegmentsOther = isAbove(
                avl[s.label - 1], s.right.y)
            belowExistOther, belowSegmentsOther = isBelow(
                avl[s.label - 1], s.right.y)

            aboveExist, aboveSegments = isAbove(avl[s.label], s.right.y)
            belowExist, belowSegments = isBelow(avl[s.label], s.right.y)

            # print("aboveExist: ", aboveExist)
            # print("belowExist: ", aboveExist)
            # print("aboveExistOther: ", aboveExistOther)
            # print("belowExistOther: ", belowExistOther)

            if (aboveExist and belowExistOther):
                for aboveSegment in aboveSegments:
                    for belowSegment in belowSegmentsOther:
                        hasIntersection = segments_intersect(
                            aboveSegment, belowSegment)
                        if (hasIntersection):
                            return True

            if (aboveExistOther and belowExist):
                for aboveSegment in aboveSegmentsOther:
                    for belowSegment in belowSegments:
                        hasIntersection = segments_intersect(
                            aboveSegment, belowSegment)
                        if (hasIntersection):
                            return True

            # remoção do segmento
            itemList = avl[s.label].get(s.left.y)
            if len(itemList) > 1:
                for i in range(len(itemList) - 1):
                    if (itemList[i] != s):
                        continue
                    itemList.pop(i)

            else:
                avl[s.label].pop(s.left.y, False)

    return False


def EnvoltoriaAleatoria(seedParam=12, numDots=20, x_inicial=0, x_final=100, y_inicial=0, y_final=100):
    dot_list = []

    seed(seedParam)
    for i in range(numDots):
        x = randint(x_inicial, x_final)
        y = noise(randint(y_inicial, y_final))
        a = Dot(x, y)
        dot_list.append(a)

    sorted_list = sortDotsByPolarAngle(dot_list)

    return (dot_list, Graham(sorted_list))


def plotEnvoltoria(ax, pontos, envoltoria, dotType='r*', envType='b-'):

    for i in range(len(pontos)):
        ax.plot(pontos[i].x, pontos[i].y, dotType)

    lista_Envoltoria = [[], []]

    for e in envoltoria:
        lista_Envoltoria[0].append(e.x)
        lista_Envoltoria[1].append(e.y)

    ax.plot(lista_Envoltoria[0], lista_Envoltoria[1], envType)
    ax.plot([lista_Envoltoria[0][len(lista_Envoltoria[0]) - 1], lista_Envoltoria[0][0]],
            [lista_Envoltoria[1][len(lista_Envoltoria[1]) - 1], lista_Envoltoria[1][0]], envType)


def preProcessConvexHull(EnvoltoriaA, EnvoltoriaB):

    endpoitsList: Endpoint = []
    segmentsList: Segment = []

    for i in range(len(EnvoltoriaA) - 1):
        dotA = EnvoltoriaA[i]
        dotB = EnvoltoriaA[i + 1]

        left = dotA if dotA.x < dotB.x else dotB
        right = dotA if dotA.x >= dotB.x else dotB

        endpoitsList.append(Endpoint(left, segmentIndx=i, endpointType='left'))
        endpoitsList.append(
            Endpoint(right, segmentIndx=i, endpointType='right'))

        segmentsList.append(Segment(left, right, 0))

    pn = EnvoltoriaA[-1]
    p0 = EnvoltoriaA[0]

    left = pn if pn.x < p0.x else p0
    right = pn if pn.x >= p0.x else p0

    segmentMax = len(segmentsList)

    endpoitsList.append(
        Endpoint(left, segmentIndx=segmentMax, endpointType='left'))
    endpoitsList.append(
        Endpoint(right, segmentIndx=segmentMax, endpointType='right'))
    segmentsList.append(Segment(left, right, 0))

    for j in range(len(EnvoltoriaA), len(EnvoltoriaA) + len(EnvoltoriaB) - 1):
        i = j - len(EnvoltoriaA)
        dotA = EnvoltoriaB[i]
        dotB = EnvoltoriaB[i + 1]

        left = dotA if dotA.x < dotB.x else dotB
        right = dotA if dotA.x >= dotB.x else dotB

        endpoitsList.append(Endpoint(left, segmentIndx=j, endpointType='left'))
        endpoitsList.append(
            Endpoint(right, segmentIndx=j, endpointType='right'))

        segmentsList.append(Segment(left, right, 1))

    pn = EnvoltoriaB[-1]
    p0 = EnvoltoriaB[0]
    left = pn if pn.x < p0.x else p0
    right = pn if pn.x >= p0.x else p0

    segmentMax = len(segmentsList)

    endpoitsList.append(
        Endpoint(left, segmentIndx=segmentMax, endpointType='left'))
    endpoitsList.append(
        Endpoint(right, segmentIndx=segmentMax, endpointType='right'))
    segmentsList.append(Segment(left, right, 1))

    endpoitsList.sort()

    return (endpoitsList, segmentsList)


def testTo(n: int):
    nPoints = 6
    fig, ax = plt.subplots(n)
    fig.set_figheight(2*n)
    plt.subplots_adjust(hspace=0.5)

    for i in range(n):
        (pontosA, EnvoltoriaA) = EnvoltoriaAleatoria(i+1, numDots=nPoints)
        (pontosB, EnvoltoriaB) = EnvoltoriaAleatoria(
            i+3, nPoints, 30, 200, 50, 200)

        plotEnvoltoria(ax[i], pontosA, EnvoltoriaA)
        plotEnvoltoria(ax[i], pontosB, EnvoltoriaB, dotType='go', envType='y-')

        endPointList, segmentsList = preProcessConvexHull(
            EnvoltoriaA=EnvoltoriaA, EnvoltoriaB=EnvoltoriaB)

        isIntercect = (sweepLineIntersection(endPointList, segmentsList))
        ax[i].set_title(isIntercect)

    plt.show()

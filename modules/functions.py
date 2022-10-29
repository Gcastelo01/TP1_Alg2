from random import randint, seed, random
import matplotlib.pyplot as plt
import bintrees
from .classes import Dot, Endpoint



class Segment:
    """
    Define um segmento de reta. Um segmento é um pedaço de uma reta que conecta 2 pontos
    @parâmetro left - Ponto inicial do segmento
    @parâmetro right - Ponto final do segmento
    @parâmetro label - Nome do segmento
    """

    def __init__(self, left: Dot, right: Dot, label):
        self.left = left
        self.right = right
        self.label = label

    def __repr__(self) -> str:
        return f'( {self.left} -> {self.right}, {self.label} )'

    def __eq__(self, other) -> bool:
        return (self.left == other.left and self.right == other.right and self.label == other.label)


def sortDotsByPolarAngle(dotsParam) -> list:
    """
    sortDotsByPolarAngle recebe uma lista de pontos não ordenada e retorna a lista com os mesmos pontos, ordenados de acordo com ângulo polar em relação ao ponto de menor y (tratado como âncora). Custo assintótico O(n log n)

    @param dotsParam: Lista de pontos não ordenados.
    @return Lista de pontos ordenados
    """
    dots = dotsParam.copy()
    anchor = dots[0]
    indx = 0
    anchor_indx = indx

    # Encontra âncora em custo O(n)
    for p in dots:
        if p.y < anchor.y:
            anchor = p
            anchor_indx = indx
        elif (p.y == anchor.y and p.x < anchor.x):
            anchor = p
            anchor_indx = indx
        indx += 1

    # Normaliza os pontos. Custo O(n)
    norm_dots = []
    dots.pop(anchor_indx)
    for dot in dots:
        norm_dots.append(dot - anchor)

    # Ordena os pontos em O(n log n)
    norm_dots.sort()

    sorted_dots = [anchor]
    for dot in norm_dots:
        sorted_dots.append(dot + anchor)

    return sorted_dots


def noise(x) -> float:
    """
    Soma a um número um determinado valor pseudoaleatório no intervalo [0, 1).
    Custo assintótico O(1)

    @param Número no qual acrescentar ruído
    @return Número com ruído 
    """
    return x + random() / 10**7


def isLeftTurn(a, b, c) -> bool:
    """
    Dados 3 pontos: a, b e c, a função verifica se há uma volta para a esquerda no caminho a -> b -> c. Custo assinstótico O(1).

    @param a: Ponto 
    @param a: Ponto 
    @param a: Ponto 
    @return bool True ou False
    """
    B = b - a
    C = c - a

    term1 = (B.x)*(C.y)
    term2 = (B.y)*(C.x)
    return (term1 - term2) > 0


def Graham(DotListParam) -> list:
    """
    Execução padrão da Varredura de Graham para definir a envoltória convexa do conjunto. Custo assintótico O(n).

    @param DotListParam: Lista de pontos ordenados pela coordenada polar em relação ao âncora

    @return list: Lista com os pontos pertencentes à envoltória convexa  
    """
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


def on_segment(p1: Dot, p2: Dot, p3: Dot) -> bool:
    """
    Verifica se o ponto p3 está na semireta p1 -> p2, ou seja, p1 -> p2 -> p3 são colineares

    @param p1: Ponto
    @param p2: Ponto
    @param p3: Ponto
    @return: bool
    """

    p1HasLessX = p1.x < p2.x
    if p1HasLessX and p1.x <= p3.x and p2.x >= p3.x:
        return True
    if p2.x <= p3.x and p1.x >= p3.x:
        return True
    return False


def direction(a, b, c) -> int:
    """ 
    Verifica a direção seguida na mudança de rotas a -> b -> c.

    @return 1 se vira a esquerda, 0 se colinear e -1 se vira à direita
    """

    B = b - a
    C = c - a

    term1 = (B.x)*(C.y)
    term2 = (B.y)*(C.x)
    return (term1 - term2)


def __aux_segments_intersect__(p1, p2, p3, p4) -> bool:
    """
    Método auxiliar para verificar se há intersecção entre dois segmentos.
    Não deve ser chamado no corpo principal das funções.
    """

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


def segments_intersect(s1: Segment, s2: Segment) -> bool:
    """
    Dados dois segmentos, verifica se há intersecção entre eles.

    @param s1: Segmento
    @param s2: Segmento

    @return bool
    """
    return __aux_segments_intersect__(s1.left, s1.right, s2.left, s2.right)


def isAbove(avl: bintrees.AVLTree, key) -> bool:
    """
    Verifica se um segmento possui algum acima dele

    """
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


def isBelow(avl, key) -> bool:
    """
    Verifica se algum segmento possui segmentos abaixo dele
    """
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


def sweepLineIntersection(endpoitsList, segmentsList) -> bool:
    """
    Algoritmo de varredura linear. Verifica se existe interesecção na lista de segmentos varridos no momento.

    @param endpoitsList: Lista de pontos finais
    @param segmentList: Lista com segmentos sendo varridos no momento
    """
    avl = [bintrees.AVLTree(), bintrees.AVLTree()]

    for p in endpoitsList:

        s = segmentsList[p.segmentIndx]

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
                    if (hasIntersection):
                        return True

            belowExist, otherSegments = isBelow(avl[s.label - 1], s.left.y)
            if (belowExist):
                for other in otherSegments:
                    hasIntersection = segments_intersect(s, other)
                    if (hasIntersection):
                        return True

        else:
            aboveExistOther, aboveSegmentsOther = isAbove(
                avl[s.label - 1], s.right.y)
            belowExistOther, belowSegmentsOther = isBelow(
                avl[s.label - 1], s.right.y)

            aboveExist, aboveSegments = isAbove(avl[s.label], s.right.y)
            belowExist, belowSegments = isBelow(avl[s.label], s.right.y)

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


def EnvoltoriaAleatoria(seedParam=12, numDots=20, x_inicial=0, x_final=100, y_inicial=0, y_final=100) -> tuple([list, list]):
    """
    Gera uma lista de pontos aleatória, e, em seguida, aplica o algoritmo de Graham nela.

    @return uma tupla contendo a lista de pontos e a lista com os pontos pertencentes à envoltória
    """
    dot_list = []

    seed(seedParam)
    for i in range(numDots):
        x = randint(x_inicial, x_final)
        y = noise(randint(y_inicial, y_final))
        a = Dot(x, y)
        dot_list.append(a)

    sorted_list = sortDotsByPolarAngle(dot_list)

    return (dot_list, Graham(sorted_list))


def plotEnvoltoria(ax, pontos, envoltoria, dotType='r*', envType='b-') -> None:
    """
    Plota a envoltória convexa no gráfico
    """
    for i in range(len(pontos)):
        ax.plot(pontos[i].x, pontos[i].y, dotType)

    lista_Envoltoria = [[], []]

    for e in envoltoria:
        lista_Envoltoria[0].append(e.x)
        lista_Envoltoria[1].append(e.y)

    ax.plot(lista_Envoltoria[0], lista_Envoltoria[1], envType)
    ax.plot([lista_Envoltoria[0][len(lista_Envoltoria[0]) - 1], lista_Envoltoria[0][0]],
            [lista_Envoltoria[1][len(lista_Envoltoria[1]) - 1], lista_Envoltoria[1][0]], envType)


def preProcessConvexHull(EnvoltoriaA, EnvoltoriaB) -> tuple:
    """
    Faz o pré processamento das envoltórias convexas.

    """
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

# ************************** Model Section ***********************************


def squareDotsDistance(dotA: Dot, dotB: Dot) -> float:
    """
    Define a distância quadrada entre dois pontos

    """
    return (dotB.x - dotA.x)**2 + (dotB.y - dotA.y)**2


def closesPoint(EnvoltoriaA, EnvoltoriaB) -> tuple([Dot, Dot]):
    """
    Dadas duas envoltórias, este método retorna o par de pontos mais próximos, sendo um pertencente à A e outro pertencente à B.
    """
    lenMin = squareDotsDistance(EnvoltoriaA[0], EnvoltoriaB[0])
    aMin = EnvoltoriaA[0]
    bMin = EnvoltoriaB[0]
    for a in EnvoltoriaA:
        for b in EnvoltoriaB:
            if squareDotsDistance(a, b) < lenMin:
                lenMin = squareDotsDistance(a, b)
                aMin = a
                bMin = b

    return aMin, bMin


def orthogonalLine(aDot, bDot, extremeX, extremeY) -> tuple([Dot, Dot]):
    """
    Dados dois pontos A e B,  determina uma linha ortogonal que divide o segmento que conecta ambos ao meio (a mediatriz).

    @param aDot: Ponto A
    @param bDot: Ponto B

    @return Uma lista contendo : Os pontos que determinam a mediatriz, os pontos A e B
    """

    left = aDot if aDot.x < bDot.x else bDot
    right = aDot if aDot.x >= bDot.x else bDot

    xMedio = (left.x + right.x)/2
    yMedio = (left.y + right.y)/2

    deltaY = (bDot.y - aDot.y)
    deltaX = (bDot.x - aDot.x)

    if deltaY == 0:
        deltaY = 0.0000001


    angCoef = - (deltaX / deltaY)
    bMediatriz = yMedio - angCoef*xMedio

    mediatrizA = Dot(extremeX[0], angCoef*(extremeX[0]) + bMediatriz)
    mediatrizB = Dot(extremeX[1], angCoef*(extremeX[1]) + bMediatriz)

    

    return (mediatrizB, mediatrizA), (angCoef, bMediatriz)


def ourModel(EnvoltoriaA, EnvoltoriaB, extremeX, extremeY) -> tuple([tuple, tuple]):
    """
    Dadas as duas envoltórias, encontra o par de pontos mais próximos e liga as duas. Em seguida, traça a ortogonal à reta de ligação. 
    """
    line = closesPoint(EnvoltoriaA, EnvoltoriaB)
    a, b = line

    orthogonal, params = orthogonalLine(a, b, extremeX, extremeY)

    # Verifica se a reta é realmente orthogonal
    c, d = orthogonal
    produtoEscalar = (b.x - a.x) * (d.x - c.x) + (b.y - a.y) * (d.y - c.y)

    assert produtoEscalar <= 10**-6, "Erro a reta encontrada não é ortogonal"

    # Verfica se a envoltoria A está a esquerda da Reta
    left =  True if direction(c, d, a) > 0 else False

    return orthogonal, line, left, params

# **************************** Test Section ************************


def testTo(n: int) -> None:
    """
    Função que testa todo o processo de funcionamento do modelo: Desde a criação de dois conjuntos de pontos aleatórios, passando pela criação das envoltórias até chegar na separação dos conjuntos.

    @param n Número de testes pseudoaleatórios a serem gerados
    
    A função não retorna nada. Ela plota os gráficos, mostrando as envoltórias.
    """
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

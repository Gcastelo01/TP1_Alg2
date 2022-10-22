from audioop import minmax
from .classes import *
from .functions import *

from sklearn.model_selection import train_test_split


def plotClass(List, ax, dotType='r*', envType='b-', compareCol1=1, compareCol2=2, withNoise=True):
    # Recebe uma tabela com duas colunas referentes ao x e y da classe

    x = []
    y = []
    dot_list = []
    for row in List.itertuples():
        a = noise(row[compareCol1]) if withNoise else row[compareCol1]
        b = noise(row[compareCol2]) if withNoise else row[compareCol2]
        dot = Dot(a, b)
        x.append(a)
        y.append(b)
        dot_list.append(dot)

    sorted_list = sortDotsByPolarAngle(dot_list)
    env = Graham(sorted_list)
    plotEnvoltoria(ax, dot_list, env, dotType=dotType, envType=envType)


def createDots(setPoints, compareCol1, compareCol2, withNoise) -> list:
    dot_list = []

    for row in setPoints.itertuples():
        a = noise(row[compareCol1]) if withNoise else row[compareCol1]
        b = noise(row[compareCol2]) if withNoise else row[compareCol2]
        dot = Dot(a, b)
        dot_list.append(dot)

    return dot_list


def classificacao(setPoints, compareCol1, compareCol2, model, whoIsLeft, whoIsRight) -> list:
    y = []

    for row in setPoints.itertuples():
        a = row[compareCol1]
        b = row[compareCol2]
        dot = Dot(a, b)

        direcao = direction(model[0], model[1], dot)

        if direcao > 0:
            y.append(whoIsLeft)
        elif direcao < 0:
            y.append(whoIsRight)
        else:
            y.append("dot is on the point")

    return y


def plotModel(X, ax, filter, rotulo, dotType='r*', envType='b-', compareCol1=1, compareCol2=2, withNoise=True, plotEnv=False):
    envoltorias = []

    # Processamento das dados e Calculas as envoltorias
    dotList = []
    setDots = [X[filter], X[~filter]]
    for points in setDots:
        dots = createDots(points, compareCol1, compareCol2, withNoise)
        sorted_list = sortDotsByPolarAngle(dots)
        envoltoria = Graham(sorted_list)
        dotList += dots
        envoltorias.append(envoltoria)
        plotEnvoltoria(ax, dots, envoltoria, dotType=dotType, envType=envType)

    # Verifica se tem Interseção
    endPointList, segmentsList = preProcessConvexHull(
        envoltorias[0], envoltorias[1])
    hasIntersection = sweepLineIntersection(endPointList, segmentsList)

    if hasIntersection:
        return "Os segmentos não são separaveis"

    # Plota o Modelo Linear
    extremeX = [dotList[0].x, dotList[0].y]
    extremeY = [dotList[0].y, dotList[0].y]

    for dot in dotList:
        if dot.x < extremeX[0] or dot.x > extremeX[1]:
            if dot.x < extremeX[0]:
                extremeX[0] = dot.x
            else:
                extremeX[1] = dot.x
            
        if dot.y < extremeY[0] or dot.y > extremeY[1]:
            if dot.y < extremeY[0]:
                extremeY[0] = dot.y
            else:
                extremeY[1] = dot.y


    model = 1
    firstConvexHullIsLeft = 1

    if (not hasIntersection):
        model, line, firstConvexHullIsLeft = ourModel(
            envoltorias[0], envoltorias[1], extremeX, extremeY)
        a, b = line
        ax.plot([a.x, b.x], [a.y, b.y], 'r-')

        c, d = model
        ax.plot([c.x, d.x], [c.y, d.y], 'r-')

    # Plota os pontos classificados
    # Este trecho só tem utlidade visual
    if not plotEnv:
        for dot in dotList:
            if direction(model[0], model[1], dot) > 0:
                ax.plot(dot.x, dot.y, 'b.')
            elif direction(model[0], model[1], dot) < 0:
                ax.plot(dot.x, dot.y, 'g.')
            else:
                ax.plot(dot.x, dot.y, 'y.')

    return (model, firstConvexHullIsLeft)


def test_train(df, label, atributeA, atributeB):
    df = df[(df[label] == atributeA) | (df[label] == atributeB)]

    y = df[label]
    X = df.drop(label, axis=1)

    return train_test_split(X, y, random_state=25, train_size=0.7, shuffle=True)

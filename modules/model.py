from audioop import minmax
from .classes import *
from .functions import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score


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


def createDots(setPoints, compareCol1=1, compareCol2=2, withNoise= True) -> list:
    dot_list = []

    for row in setPoints.itertuples():
        a = noise(row[compareCol1]) if withNoise else row[compareCol1]
        b = noise(row[compareCol2]) if withNoise else row[compareCol2]
        dot = Dot(a, b)
        dot_list.append(dot)

    return dot_list


def classificacao(setPoints, model, whoIsLeft, whoIsRight) -> list:
    y = []

    for row in setPoints.itertuples():
        a = row[1]
        b = row[2]
        dot = Dot(a, b)

        direcao = direction(model[0], model[1], dot)

        if direcao >= 0:
            y.append(whoIsLeft)
        elif direcao < 0:
            y.append(whoIsRight)

    return y


def plotModel(X, ax, filter, rotulo, dotType= ['r*', 'y.'], envType= ['b-', 'g-'], withNoise=True, plotEnv=False, modelAjust=0):
    envoltorias = []

    # Processamento das dados e Calculas as envoltorias
    dotList, envoltorias = plotEnvoltorias(X, ax, filter, rotulo, dotType=dotType, envType=envType, withNoise=withNoise)

    # Scala da Reta encontra o menor a maior x
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

    model, line, firstConvexHullIsLeft = ourModel(
        envoltorias[0], envoltorias[1], extremeX, extremeY)
    a, b = line



    ax.plot([a.x, b.x], [a.y, b.y], 'r-')

    c, d = model
    alphaLine = (d.y - c.y) / (d.x - c.x)
    betaLine = c.y - alphaLine*c.x
    median = Dot((a.x + b.x)/2, (a.y + b.y)/2)
    lineSize = ((b.y - a.y)**2 + (b.x - a.x)**2)**0.5

    cNorm = Dot(median.x - (lineSize + modelAjust), alphaLine*(median.x - (lineSize + modelAjust)) + betaLine)
    dNorm = Dot(median.x + (lineSize + modelAjust), alphaLine*(median.x + (lineSize + modelAjust)) + betaLine)
    ax.plot([cNorm.x, dNorm.x], [cNorm.y, dNorm.y], 'v-')
    # ax.plot([c.x, d.x], [c.y, d.y], 'v-')

    return (model, firstConvexHullIsLeft)


def test_train(df, label, atributeA, atributeB):
    df = df[(df[label] == atributeA) | (df[label] == atributeB)]

    y = df[label]
    X = df.drop(label, axis=1)

    return train_test_split(X, y, random_state=25, train_size=0.7, shuffle=True)

def plotEnvoltorias(X, ax, filter, rotulo, dotType= ['r*', 'g.'], envType= ['b-', 'y-'], withNoise=True):
    envoltorias = []

    # Processamento das dados e Calculas as envoltorias
    dotList = []
    setDots = [X[filter], X[~filter]]
    for i in range(2):
        dots = createDots(setDots[i], withNoise=withNoise)
        sorted_list = sortDotsByPolarAngle(dots)
        envoltoria = Graham(sorted_list)
        dotList += dots
        envoltorias.append(envoltoria)
        plotEnvoltoria(ax, dots, envoltoria, dotType=dotType[i], envType=envType[i])
    
    return dotList, envoltorias
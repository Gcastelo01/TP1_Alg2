class Dot:
    """
    Representa um ponto bidimensional no plano cartesiano.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, b):
        """
        Compara dois pontos, e determina se um é menor que o outro
        """
        A = (self.x)*(b.y)
        B = (self.y)*(b.x)
        return (A - B) > 0

    def __sub__(self, b):
        """
        Retorna a diferença entre 2 pontos

        @param b: Ponto
        """
        return Dot(self.x - b.x, self.y - b.y)

    def __add__(self, b):
        """
        Retorna a soma de 2 pontos

        @param b: Ponto
        """
        return Dot(self.x + b.x, self.y + b.y)

    def __repr__(self) -> str:
        """
        Representação em string de um ponto
        """
        return f'({self.x}, {self.y})'

    def __eq__(self, other) -> bool:
        """
        Compara dois pontos, e determina se são iguais.

        @param other: Ponto
        """
        if (self.x == other.x and self.y == other.x):
            return True
        return False


class Endpoint(Dot):
    """
    
    """
    def __init__(self, dot: Dot, segmentIndx,  endpointType: str):
        # endpoit type = 'left' | 'right'
        self.dot = dot
        self.segmentIndx = segmentIndx
        self.endpointType = endpointType

    def __repr__(self):
        return f'({self.dot}, {self.segmentIndx}, {self.endpointType})'

    def __lt__(self, b):
        """
        Compara 2 Endpoints e retorna o operador menor que entre eles
        """
        if self.dot.x == b.dot.x:
            if self.endpointType == b.endpointType:
                return self.dot.y < b.dot.y
            else:
                return True if self.endpointType == 'left' else False
        else:
            return self.dot.x < b.dot.x

    def __eq__(self, other):
        """
        Compara 2 endpoints e verifica se são iguais
        """
        if (self.dot == other.dot and self.segmentIndx == other.segmentIndx and self.endpointType == other.endpointType):
            return True
        return False


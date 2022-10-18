class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, b):
        A = (self.x)*(b.y)
        B = (self.y)*(b.x)
        return (A - B) > 0

    def __sub__(self, b):
        return Dot(self.x - b.x, self.y - b.y)

    def __add__(self, b):
        return Dot(self.x + b.x, self.y + b.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        if (self.x == other.x and self.y == other.x):
            return True
        return False


class Endpoint:
    def __init__(self, dot: Dot, segmentIndx,  endpointType):
        # endpoit type = 'left' | 'right'
        self.dot = dot
        self.segmentIndx = segmentIndx
        self.endpointType = endpointType

    def __repr__(self):
        return f'({self.dot}, {self.segmentIndx}, {self.endpointType})'

    def __lt__(self, b):
        if self.dot.x == b.dot.x:
            if self.endpointType == b.endpointType:
                return self.dot.y < b.dot.y
            else:
                return True if self.endpointType == 'left' else False
        else:
            return self.dot.x < b.dot.x

    def __eq__(self, other):
        if (self.dot == other.dot and self.segmentIndx == other.segmentIndx and self.endpointType == other.endpointType):
            return True
        return False


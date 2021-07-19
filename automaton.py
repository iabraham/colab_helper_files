from collections import deque

class Automaton:

    def __init__(self, alphabets, start, cw):
        if len(set(alphabets)) < len(alphabets):
            raise ValueError('Alphabet must be unique')
        else:
            self.alphabets = alphabets
            self.start = start
            pot_cw = deque(cw)
            while pot_cw[0] != start:
                pot_cw.rotate(1)
            self.cw = "".join(pot_cw)
            for x in ["prev_state", "state", "path"]:
                setattr(self, x, None)

    def __repr__(self):
        if self.path is None:
            return "Automaton(unset)"
        else:
            return "Automaton({p},{c})".format(p=self.prev_state, c=self.state)

    def setPath(self, path):
        if isinstance(path, str):
            path = list(path)
        elif isinstance(path, list):
            pass
        else:
            raise TypeError("Path must be a string representing a path or a list\
                    of alphabets representing a path")
        
        if not all(x in self.alphabets for x in path):
            raise LookupError("Path contains non-alphabet characters")
        if path[0] != self.start:
            raise IndexError("Path does not start at expected source node")
        if path[0] != path[-1]:
            raise TypeError("Path is not closed")

        *self.path, = reversed(path)
        return self

    def __step(self):
        if self.path is None:
            raise ValueError("No path set to step")
        else:
            self.prev_state = self.state
            self.state = self.path.pop()

        return self

    def walkPath(self):
        winding_no = list()
        visited = set()
        if self.path is None:
            raise ValueError("No path set to walk")
        else:
            winding_no.append(0)
            while self.path != []:
                _ = self.__step()
                if len(visited)>1 and self.state == self.start:
                    if self.prev_state == self.cw[-1]:
                        winding_no.append(winding_no[-1]-1)
                        visited = set()
                    elif self.prev_state == self.cw[1]:
                        winding_no.append(winding_no[-1]+1)
                        visited = set()
                    else:
                        winding_no.append(winding_no[-1])
                else:
                    visited.add(self.state)
                    winding_no.append(winding_no[-1])

        return winding_no



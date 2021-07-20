from collections import deque


class Automaton:
    """Class to sort of represent a tape reader/Turing machine."""

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
            for x in ["prev_state", "state", "path", "entry", "exit"]:
                setattr(self, x, None)

    def __repr__(self):
        """Represent automaton's current state."""
        if self.path is None:
            return "Automaton(unset)"
        else:
            return "Automaton({p},{c})".format(p=self.prev_state, c=self.state)

    def setPath(self, path):
        """Set the path/tape for the machine to read."""
        if isinstance(path, str):
            path = list(path)
        elif isinstance(path, list):
            pass
        else:
            raise TypeError("Path must be a string representing a path or a\
                            list of alphabets representing a path")

        if not all(x in self.alphabets for x in path):
            raise LookupError("Path contains non-alphabet characters")

        *self.path, = reversed(path)
        return self

    def __step(self):
        """Read one item in the tape, take one step on the path."""
        if self.path is None:
            raise ValueError("No path set to step")
        else:
            self.prev_state = self.state
            self.state = self.path.pop()

        return self

    def __reset_ee(self):
        self.entry, self.exit = None, None

    def _get_ee(self):
        return (self.exit, self.entry)

    def walkPath(self):
        """Read the tape a.k.a walk the path."""
        winding_no, walking = [0], False
        plusminus = {(self.cw[1], self.cw[-1]): -1,
                     (self.cw[-1], self.cw[1]): +1}

        if self.path is None:
            raise ValueError("No path set to walk")
        else:
            while self.path != []:
                _ = self.__step()
                # Either left homebase, entered homebase or still walking
                if self.prev_state == self.start and self.state != self.start:
                    self.exit, walking = self.state, True
                elif walking and self.state == self.start:
                    self.entry, walking = self.prev_state, False
                else:
                    curr_winding = winding_no[-1]

                try:  # If at homebase
                    curr_winding = winding_no[-1] + plusminus[self._get_ee()]
                    self.__reset_ee()
                except KeyError:  # Not at homebase
                    pass

                winding_no.append(curr_winding)

        return winding_no

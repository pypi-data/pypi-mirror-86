import typing
from cgshop2021_pyutils.solution.direction import Direction


class SolutionStep:
    """
    A single step of a solution. __getitem__ and __setitem__ are defined
    such that for any robot, the direction can be obtained and set.
    Iteration over a solution step will iterate over all robots that actually move.
    """
    def __init__(self, index: int = None, directions: typing.Optional[typing.Dict[int, Direction]] = None):
        self.index = index
        self._directions = {} if directions is None else {r: d for r, d in directions.items() if d != Direction.WAIT}

    def __setitem__(self, robot_id: int, direction: Direction):
        if direction == Direction.WAIT:
            try:
                del self._directions[robot_id]
            except KeyError:
                pass
        else:
            self._directions[robot_id] = direction

    def __getitem__(self, robot_id: int) -> Direction:
        return self._directions.get(robot_id, Direction.WAIT)

    def __len__(self):
        return len(self._directions)

    def __iter__(self):
        return iter(self._directions.items())

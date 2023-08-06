from typing import Tuple, Optional, Dict, List


class InstanceBuilder:
    """
    Builds an instance by adding obstacles and robots one-by-one.
    """
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.id_counter = 0
        self.name = name
        self.description = description
        self.robots = []
        self.obstacles = []
        self.at_position = {}

    def _allocate_id(self):
        result = self.id_counter
        self.id_counter += 1
        return result

    def add_robot(self, start: Tuple[int,int], target: Tuple[int,int]):
        start_type = 'start'
        target_type = 'target'
        if start in self.at_position:
            if self.at_position[start][0] != 'target':
                raise ValueError("Start position of robot is already occupied!")
            else:
                start_type = 'both'
        if target in self.at_position:
            if self.at_position[target][0] != 'start':
                raise ValueError("Target position of robot is already occupied!")
            else:
                target_type = 'both'
        robot_id = self._allocate_id()
        self.at_position[start] = (start_type, robot_id)
        self.at_position[target] = (target_type, robot_id)
        self.robots.append([start, target])

    def add_obstacle(self, position: Tuple[int,int]):
        if position in self.at_position:
            raise ValueError("Obstacle position is already occupied!")
        self.at_position[position] = ('obstacle', len(self.obstacles))
        self.obstacles.append(position)

    def build_instance(self) -> 'Instance':
        result = Instance(self.name, self.description)
        result.number_of_robots = len(self.robots)
        result.start = [s for s, t in self.robots]
        result.target = [t for s, t in self.robots]
        result.obstacles = list(self.obstacles)
        result.at_position = dict(self.at_position)
        return result


class Instance:
    """
    Instances need to encode the origin and target for all robots.
    Robots have ids starting at 0.
    There can also be obstacles.
    """
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.start: List[Tuple[int,int]] = []
        self.target: List[Tuple[int,int]] = []
        self.obstacles: List[Tuple[int,int]] = []
        self.at_position: Dict[Tuple[int,int], Tuple[str,int]] = {}
        self.number_of_robots = 0
        self.name = name
        self.description = description

    def start_of(self, robot_id: int) -> Tuple[int, int]:
        return self.start[robot_id]

    def target_of(self, robot_id: int) -> Tuple[int, int]:
        return self.target[robot_id]

    def is_obstacle(self, position: Tuple[int, int]):
        return position in self.at_position and self.at_position[position][0] == 'obstacle'

    def __repr__(self):
        return f"CG:SHOP2021.Instance(name={self.name})"

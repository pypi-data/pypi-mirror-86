from typing import Tuple
from cgshop2021_pyutils.instance import Instance


class InvalidSolutionError(RuntimeError):
    def __init__(self, instance, solution, message):
        super().__init__(message)
        self.instance = instance
        self.solution = solution


class RobotCollisionError(InvalidSolutionError):
    def __init__(self, instance: Instance, solution: 'Solution', robots: Tuple[int,int],
                 step: 'SolutionStep', position: Tuple[int,int]):
        self.step = step
        self.robots = robots
        self.position = position
        super().__init__(instance, solution,
                         f'In step {step.index}, robot {robots[0]} collides with robot {robots[1]} at position {position}!')


class ObstacleCollisionError(InvalidSolutionError):
    def __init__(self, instance: Instance, solution: 'Solution', step: 'SolutionStep', robot: int, position):
        self.step = step
        self.robot = robot
        self.position = position
        super().__init__(instance, solution,
                         f'In step {step.index}, robot {robot} moves into the obstacle at position {position}!')


class TargetNotReachedError(InvalidSolutionError):
    def __init__(self, instance, solution, end_positions):
        self.end_positions = end_positions
        super().__init__(instance, solution,
                         'The solution is collision-free but does not reach the target configuration!')


class UnknownInstanceError(RuntimeError):
    def __init__(self, instance_name):
        self.instance_name = instance_name
        super().__init__(f'The instance name {instance_name} does not correspond to any known instance!')

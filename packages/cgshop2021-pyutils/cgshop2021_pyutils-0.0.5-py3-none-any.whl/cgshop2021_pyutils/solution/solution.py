from typing import Optional, List, Tuple, Iterable, Dict, Union
from cgshop2021_pyutils.instance import Instance
from cgshop2021_pyutils.solution.solution_step import SolutionStep
from cgshop2021_pyutils.solution import ObstacleCollisionError, RobotCollisionError


class _StepPerformer:
    def __init__(self, config: 'RobotConfiguration', step: SolutionStep):
        self.step = step
        self.config = config
        self.new_index = step.index + 1
        self.old_positions = self.config.positions
        self.old_at = self.config.at_positions
        self.new_positions = list(self.config.positions)
        self.new_at = dict(self.config.at_positions)

    def _check_target_for_obstacle(self, robot, target):
        if self.config.is_obstacle(target):
            raise ObstacleCollisionError(self.config.instance, self.config.solution,
                                         self.step, robot, target)

    def _check_target_for_robot(self, robot, target):
        target_robot = self.config.robot_at_position(target)
        if target_robot is not None:
            if self.step[target_robot] != self.step[robot]:
                # It's a collision if target_robot does not move in the same direction as us.
                raise RobotCollisionError(self.config.instance, self.config.solution,
                                          (robot, target_robot), self.step, target)
        return target_robot

    def _check_for_multiple_robots(self, robot, target, target_robot):
        new_target_robot = self.new_at.get(target, target_robot)
        if new_target_robot != target_robot:
            # more than one robot trying to move into target
            raise RobotCollisionError(self.config.instance, self.config.solution,
                                      (robot, new_target_robot), self.step, target)

    def perform_step(self):
        for robot, direction in self.step:
            spos = self.old_positions[robot]
            tpos = (spos[0] + direction.value[0], spos[1] + direction.value[1])
            self._check_target_for_obstacle(robot, tpos)
            target_robot = self._check_target_for_robot(robot, tpos)
            self._check_for_multiple_robots(robot, tpos, target_robot)
            self.new_at[tpos] = robot
            if self.new_at[spos] == robot:
                del self.new_at[spos]
            self.new_positions[robot] = tpos
        return RobotConfiguration(self.config.instance, self.config.solution,
                                  self.new_index, self.new_positions, self.new_at)


class RobotConfiguration:
    @staticmethod
    def initial_configuration(instance, solution) -> 'RobotConfiguration':
        positions = instance.start
        at_positions = {coords: -1 for coords in instance.obstacles}
        at_positions.update(((coords, rid) for rid, coords in enumerate(instance.start)))
        return RobotConfiguration(instance, solution, 0, positions, at_positions)

    def __init__(self, instance, solution, before_step_index,
                 positions: List[Tuple[int, int]],
                 at_positions: Dict[Tuple[int, int], int]):
        self.before_step_index = before_step_index
        self.instance = instance
        self.solution = solution
        self.before_step = None if before_step_index == len(solution.steps) else \
        solution.steps[before_step_index]
        self.positions = positions
        self.at_positions = at_positions

    def is_obstacle(self, position: Tuple[int, int]):
        return self.at_positions.get(position, 0) < 0

    def robot_at_position(self, position: Tuple[int, int]):
        r = self.at_positions.get(position, -1)
        return None if r < 0 else r

    def perform_step(self, step: SolutionStep) -> 'RobotConfiguration':
        p = _StepPerformer(self, step)
        return p.perform_step()


class Solution:
    """
    A class that represents a solution to an instance.
    A solution consists of several steps; each step moves a subset of the robots
    to an adjacent grid position.
    """

    def __init__(self, instance: Union[str, Instance],
                 steps: Optional[Iterable[SolutionStep]] = None, meta_data: dict = None):
        self.instance = instance
        self.steps: List[SolutionStep] = [] if steps is None else list(steps)
        self.meta_data = meta_data if meta_data else {}

    @property
    def makespan(self) -> int:
        return len(self.steps)

    @property
    def total_moves(self) -> int:
        return sum((len(s) for s in self.steps))

    def add_step(self, step: SolutionStep):
        """
        Add a step to this solution.
        :param step: The solution step to add.
        """
        step.index = len(self.steps)
        self.steps.append(step)

    def configuration_sequence(self):
        """
        Iterate through the sequence of configurations induced by the given
        instance and this solution. The intention here is to avoid
        to use too much memory by storing all intermediate configurations
        in memory simultaneously.
        """
        current = RobotConfiguration.initial_configuration(self.instance, self)
        yield current
        for s in self.steps:
            current = current.perform_step(s)
            yield current


    def __str__(self):
        return f"Solution({self.instance}, MAX={self.makespan}, SUM={self.total_moves})"

from cgshop2021_pyutils.solution.solution_step import SolutionStep
from cgshop2021_pyutils.solution import Solution
from cgshop2021_pyutils.solution.direction import Direction
import json


_DIRECTION_MAP = {Direction.EAST: 'E', Direction.WEST: 'W',
                  Direction.NORTH: 'N', Direction.SOUTH: 'S'}


class SolutionWriter:
    def _step_to_dict(self, step: SolutionStep):
        return {str(robot): _DIRECTION_MAP[direction] for robot, direction in step}

    def to_json_obj(self, solution: Solution):
        return {
            'instance': solution.instance.name,
            'steps': [self._step_to_dict(s) for s in solution.steps]
        }

    def to_json_str(self, solution: Solution):
        return json.dumps(self.to_json_obj(solution))

    def to_json_file(self, path, solution: Solution):
        with open(path, 'w') as f:
            return json.dump(self.to_json_obj(solution), f)

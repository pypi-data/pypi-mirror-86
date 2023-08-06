from cgshop2021_pyutils.solution.solution_step import SolutionStep
from cgshop2021_pyutils.solution import Solution
from cgshop2021_pyutils.solution.direction import Direction
from cgshop2021_pyutils.instance import InstanceReader, InvalidInstanceError
import json
import os

_DIRECTION_MAP = {'E': Direction.EAST, 'W': Direction.WEST,
                  'N': Direction.NORTH, 'S': Direction.SOUTH}


class SolutionEncodingError(RuntimeError):
    pass


class DirectoryInstanceCache:
    """
    An instance cache that finds all (potential) instances
    below a given directory (recursively looking into subdirectories).
    It can either load all instances on creation (load_all=True) or
    lazily load instances by their file name (load_all=False).
    """

    def _find_instance_files(self):
        result = {}
        for root, subdirs, files in os.walk(self.path):
            for f in files:
                base, ext = os.path.splitext(f)
                if ext.lower() == '.json':
                    result[base.lower()] = os.path.join(root, f)
        return result

    def _load_all(self):
        for f in self.files.values():
            try:
                instance = InstanceReader().from_json_file(f)
                self.instances[instance.name] = instance
            except (
            OSError, json.JSONDecodeError, RuntimeError, InvalidInstanceError) as e:
                pass

    def __init__(self, path, load_all=False):
        self.path = path
        self.load_all = load_all
        self.instances = {}
        self.files = self._find_instance_files()
        if self.load_all:
            self._load_all()

    def __getitem__(self, instance_name):
        if instance_name in self.instances:
            return self.instances[instance_name]
        if self.load_all or instance_name not in self.files:
            raise KeyError(instance_name)
        instance = InstanceReader().from_json_file(self.files[instance_name])
        self.instances[instance_name] = instance
        return instance


class SolutionReader:
    def __init__(self, instance_cache):
        """
        Create a new solution reader.
        It uses the given instance cache to look up instances from their names.
        The instance_cache can be a dict mapping instance names to instances,
        or any other type that allows to look up instances by cache[instance_name].
        """
        self.instances = instance_cache
        self._n_robots = 0

    @staticmethod
    def _expect_type(in_obj, key, t, in_obj_name):
        if key not in in_obj:
            raise SolutionEncodingError(f'The solution is missing the attribute "{key}"!')
        result = in_obj[key]
        if not isinstance(result, t):
            raise SolutionEncodingError(
                f'{in_obj_name}\'s attribute "{key}" is not a {str(t)}!')
        return result

    def _to_solution_step(self, step_obj):
        if not isinstance(step_obj, dict):
            raise SolutionEncodingError(
                f'The solution contains an invalid step (not an object)!')
        result = SolutionStep(-1)
        for key, value in step_obj.items():
            try:
                robot_id = int(key)
                if robot_id < 0 or robot_id >= self._n_robots:
                    raise SolutionEncodingError(
                        f'The robot id {robot_id} is out of range!')
                if value not in _DIRECTION_MAP:
                    raise SolutionEncodingError(f'The direction "{value}" is invalid!')
                direction = _DIRECTION_MAP[value]
                result[robot_id] = direction
            except ValueError:
                raise SolutionEncodingError(
                    f'A step in the solution contains an attribute that is not an integer!')
        return result

    def from_json_obj(self, obj):
        if not isinstance(obj, dict):
            raise SolutionEncodingError('Solution does not contain a unique JSON object!')
        instance_name = SolutionReader._expect_type(obj, 'instance', str, 'The solution')
        try:
            instance = self.instances[instance_name]
        except KeyError:
            raise SolutionEncodingError(
                f'Solution is for an unknown instance: "{instance_name}".')
        steps = SolutionReader._expect_type(obj, 'steps', list, 'The solution')
        solution = Solution(instance)
        self._n_robots = instance.number_of_robots
        for s in steps:
            solution.add_step(self._to_solution_step(s))
        return solution

    def from_json_str(self, data):
        return self.from_json_obj(json.loads(data))

    def from_json_file(self, path):
        with open(path, 'r') as f:
            return self.from_json_obj(json.load(f))

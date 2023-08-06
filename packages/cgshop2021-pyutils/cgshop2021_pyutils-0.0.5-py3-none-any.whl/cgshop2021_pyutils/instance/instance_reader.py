from . import InstanceBuilder, Instance
import json
from typing import Optional, Tuple
from os.path import basename


class InvalidInstanceError(Exception):
    pass


class InstanceReader:
    def __init__(self):
        self.source_path: Optional[str] = None
        self.source_name: Optional[str] = None

    def _read_meta(self, data) -> Tuple[str, str]:
        name = self.source_name
        description = None
        if self._expected_type(data, 'name', str):
            name = data['name']
        if self._expected_type(data, 'meta', dict):
            meta = data['meta']
            if 'description' in meta:
                description = meta['description']
        return name, description

    def _expected_type(self, in_dict, name, expected_type):
        return name in in_dict and isinstance(in_dict[name], expected_type)

    def _check_position(self, position):
        if not isinstance(position, list) or len(position) != 2 or \
           not isinstance(position[0], int) or not isinstance(position[1], int):
            raise InvalidInstanceError(f'Invalid position "{position}"!')
        return position[0], position[1]

    def _add_obstacles(self, builder, data):
        if not self._expected_type(data, 'obstacles', list):
            raise InvalidInstanceError('Missing or invalid obstacle list!')
        for obstacle in data['obstacles']:
            obstacle = self._check_position(obstacle)
            builder.add_obstacle(obstacle)

    def _check_starts_targets(self, data):
        if not self._expected_type(data, 'starts', list):
            raise InvalidInstanceError('Missing or invalid robot start positions!')
        if not self._expected_type(data, 'targets', list):
            raise InvalidInstanceError('Missing or invalid robot target positions!')
        starts = data['starts']
        targets = data['targets']
        if len(starts) != len(targets):
            raise InvalidInstanceError('List of start and target positions do not have the same length!')
        return starts, targets

    def _add_robots(self, builder, data):
        starts, targets = self._check_starts_targets(data)
        for s, t in zip(starts, targets):
            s = self._check_position(s)
            t = self._check_position(t)
            builder.add_robot(s, t)

    def from_json_obj(self, data: dict) -> Instance:
        if not isinstance(data, dict):
            raise InvalidInstanceError('JSON does not contain a single object!')
        name, description = self._read_meta(data)
        builder = InstanceBuilder(name, description)
        self._add_obstacles(builder, data)
        self._add_robots(builder, data)
        return builder.build_instance()

    def from_json_str(self, data: str) -> Instance:
        parsed = json.loads(data)
        return self.from_json_obj(parsed)

    def from_json_stream(self, stream):
        parsed = json.load(stream)
        return self.from_json_obj(parsed)

    def from_json_file(self, path) -> Instance:
        with open(path, 'r') as file:
            self.source_path = path
            self.source_name = basename(path)
            obj = json.load(file)
            return self.from_json_obj(obj)

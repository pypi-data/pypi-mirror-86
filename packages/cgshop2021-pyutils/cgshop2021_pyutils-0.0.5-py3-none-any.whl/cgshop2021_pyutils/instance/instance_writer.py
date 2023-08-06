import os

from . import Instance
from typing import Optional
from os.path import basename
import json


class InstanceWriter:
    def __init__(self):
        self.target_name: Optional[str] = None

    def _export_obstacles(self, instance: Instance):
        return [[obs[0], obs[1]] for obs in instance.obstacles]

    def _export_robots(self, instance: Instance):
        return [[s[0], s[1]] for s in instance.start], [[t[0], t[1]] for t in instance.target]

    def to_json_obj(self, instance: Instance):
        root = {'meta': {'number_of_robots': instance.number_of_robots}}
        if instance.description:
            root['meta']['description'] = instance.description
        if instance.name or self.target_name:
            root['name'] = instance.name or self.target_name
        root['obstacles'] = self._export_obstacles(instance)
        root['starts'], root['targets'] = self._export_robots(instance)
        return root

    def to_json_str(self, instance: Instance) -> str:
        obj = self.to_json_obj(instance)
        return json.dumps(obj)

    def to_json_file(self, path, instance):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            self.target_name = basename(path)
            obj = self.to_json_obj(instance)
            json.dump(obj, file)

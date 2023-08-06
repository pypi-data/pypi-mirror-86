import zipfile
import os
from typing import Union, Iterable
from .solution import Solution
from .solution_writer import SolutionWriter


class SolutionZipWriter:
    """
    This class allows to write solutions to a submittable zip.
    You can use
    ```
    from cgshop2021_pyutils import SolutionZipWriter
    with SolutionZipWriter("my_zip.zip") as zipper:
        zipper.add_solutions(solution_set)
        zipper.add_solution(single_solution)
    ```
    """

    def __init__(self, path: Union[str, os.PathLike], mode="x",
                 compression=zipfile.ZIP_DEFLATED, compresslevel=None):
        self.path = path
        self.mode = mode
        self.compression = compression
        if compression == zipfile.ZIP_DEFLATED and compresslevel is None:
            compresslevel = 9
        self.compresslevel = compresslevel
        try:
            self._zip_file = zipfile.ZipFile(path, mode=mode, compression=compression,
                                             compresslevel=self.compresslevel)
        except TypeError:
            # python 3.6 raises a TypeError due to compresslevel parameter missing. Use default instead.
            self._zip_file = zipfile.ZipFile(path, mode=mode, compression=compression)
        self._sol_writer = SolutionWriter()

    def __enter__(self):
        return self

    def __exit__(self, t, v, trace):
        self._zip_file.close()

    def add_solution(self, solution: Solution):
        """
        Add solution to zip
        :param solution: solution
        :return: None
        """
        instance = solution.instance.name
        # We have to objectives so we do not have a clear best solution for each instance.
        # We need to accept multiple solutions for the same instance. Thus, the
        # complicated name
        name_in_zip = f"solutions/{instance}_SOLUTION_SUM{solution.total_moves}_MS{solution.makespan}.json"
        solution_str = self._sol_writer.to_json_str(solution=solution)
        self._zip_file.writestr(name_in_zip, solution_str)

    def add_solutions(self, solutions: Iterable[Solution]):
        """
        Add solutions to zip.
        :param solutions: Iterable[Solution]
        :return: None
        """
        if isinstance(solutions, Solution):
            solutions = [solutions]
        for s in solutions:
            self.add_solution(s)

    @staticmethod
    def dump(solutions: Iterable[Solution],
             path: Union[str, os.PathLike], mode="x",
             compression=zipfile.ZIP_DEFLATED, compresslevel=None):
        with SolutionZipWriter(path, mode=mode, compression=compression,
                               compresslevel=compresslevel) as zip_writer:
            zip_writer.add_solutions(solutions)

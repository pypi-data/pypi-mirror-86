from cgshop2021_pyutils.solution import Solution
from cgshop2021_pyutils.solution import TargetNotReachedError


def __last(iter):
    last = None
    for i in iter:
        last = i
    return last

def validate(solution: Solution):
    """
    Attempts to validate an instance, raising an exception
    derived from InvalidSolutionError with further information about the error
    for invalid solutions.
    """
    last_config = __last(solution.configuration_sequence())
    if last_config.positions != solution.instance.target:
        raise TargetNotReachedError(solution.instance, solution,
                                    last_config.positions)

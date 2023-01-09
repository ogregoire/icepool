"""Evaluators for poker/Yahtzee-like mechanics."""

__docformat__ = 'google'

import icepool
from icepool.evaluator.outcome_count_evaluator import OutcomeCountEvaluator

from icepool.typing import Outcome, Order
from typing import Any


class HighestOutcomeAndCountEvaluator(OutcomeCountEvaluator[Outcome, tuple[Any,
                                                                           int],
                                                            int]):
    """The highest outcome that has positive count, along with that count.

    If no outcomes have positive count, an arbitrary outcome will be produced
    with a 0 count.
    """

    def next_state(self, state, outcome, count):
        """Implementation."""
        count = max(count, 0)
        if state is None:
            return outcome, count
        elif count > 0:
            if state[1] > 0:
                return max(state, (outcome, count))
            else:
                return outcome, count
        else:
            return state

    def order(self, *_):
        """Allows any order."""
        return Order.Any


class AllCountsEvaluator(OutcomeCountEvaluator[Outcome, tuple[int, ...], int]):
    """All counts in ascending order.

    In other words, this produces tuples of the sizes of all matching sets.
    """

    def __init__(self, *, positive_only: bool = True):
        """
        Args:
            positive_only: If `True` (default), any zero and negative values
                in the result are removed.
        """
        self._positive_only = positive_only

    def next_state(self, state, outcome, count):
        """Implementation."""
        state = (state or ()) + (count,)
        return tuple(sorted(state))

    def final_outcome(self, final_state, *_):
        """Implementation."""
        if final_state is None:
            return ()
        if self._positive_only:
            return tuple(x for x in final_state if x > 0)
        else:
            return final_state

    def order(self, *_):
        """Allows any order."""
        return Order.Any


class LargestCountEvaluator(OutcomeCountEvaluator[Outcome, int, int]):
    """The largest count of any outcome."""

    def next_state(self, state, _, count):
        """Implementation."""
        return max(state or count, count)

    def order(self, *_):
        """Allows any order."""
        return Order.Any


class LargestCountAndOutcomeEvaluator(OutcomeCountEvaluator[Outcome, tuple[int,
                                                                           Any],
                                                            int]):
    """The largest count of any outcome, along with that outcome."""

    def next_state(self, state, outcome, count):
        """Implementation."""
        return max(state or (count, outcome), (count, outcome))

    def order(self, *_):
        """Allows any order."""
        return Order.Any


class LargestStraightEvaluator(OutcomeCountEvaluator[int, int, int]):

    def next_state(self, state, _, count):
        """Implementation."""
        best_run, run = state or (0, 0)
        if count >= 1:
            run += 1
        else:
            run = 0
        return max(best_run, run), run

    def final_outcome(self, final_state, *_):
        """Implementation."""
        if final_state is None:
            return 0
        return final_state[0]

    def order(self, *_):
        """Ascending order."""
        return Order.Ascending

    alignment = OutcomeCountEvaluator.range_alignment


class LargestStraightAndOutcomeEvaluator(OutcomeCountEvaluator[int, tuple[int,
                                                                          int],
                                                               int]):

    def next_state(self, state, outcome, count):
        """Implementation."""
        best_run_and_outcome, run = state or ((0, outcome), 0)
        if count >= 1:
            run += 1
        else:
            run = 0
        return max(best_run_and_outcome, (run, outcome)), run

    def final_outcome(self, final_state, *_):
        """Implementation."""
        return final_state[0]

    def order(self, *_):
        """Ascending order."""
        return Order.Ascending

    alignment = OutcomeCountEvaluator.range_alignment

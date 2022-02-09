import _context

import hdroller
import pytest

class SumRerollIfAnyOnes(hdroller.EvalPool):
    def next_state(self, state, outcome, count):
        if outcome == 1 and count > 0:
            return None
        elif state is None:
            return outcome * count
        else:
            return state + outcome * count

def test_reroll():
    result = SumRerollIfAnyOnes().eval(hdroller.d6.pool(5))
    expected = 5 @ (hdroller.d5+1)
    assert result.equals(expected)

class SumPoolDescending(hdroller.SumPool):
    def direction(self, pool):
        return -1

def test_sum_descending():
    result = SumPoolDescending().eval(hdroller.d6.pool(5))
    expected = 5 @ hdroller.d6
    assert result.equals(expected)

def test_sum_descending_limit_outcomes():
    result = -SumPoolDescending().eval((-hdroller.d12).pool(min_outcomes=[-8, -6]))
    expected = hdroller.d6 + hdroller.d8
    assert result.equals(expected)

def test_sum_descending_keep_highest():
    result = SumPoolDescending().eval(hdroller.d6.pool()[0, 1, 1, 1])
    expected = hdroller.d6.keep_highest(4, 3)
    assert result.equals(expected)

def test_zero_weight_outcomes():
    result = hdroller.Die([0, 1, 0, 1, 0], min_outcome=0).keep_highest(3, 2)
    assert len(result) == 9

class EvalDirection(hdroller.EvalPool):
    def __init__(self, direction):
        self._direction = direction

    def next_state(self, state, outcome, count):
        return 0
    
    def direction(self, *pools):
        return self._direction

def test_direction():
    assert SumRerollIfAnyOnes().direction(hdroller.d6.pool(count_dice=[0,1,1,1])) > 0
    assert SumRerollIfAnyOnes().direction(hdroller.d6.pool(count_dice=[1,1,1,0])) < 0
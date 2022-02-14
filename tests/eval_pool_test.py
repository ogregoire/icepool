import _context

import hdroller
import pytest

class SumRerollIfAnyOnes(hdroller.EvalPool):
    def next_state(self, state, outcome, count):
        if outcome == 1 and count > 0:
            return hdroller.Reroll
        elif state is None:
            return outcome * count
        else:
            return state + outcome * count
    
    def direction(self, *_):
        return 0

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
    assert result.num_outcomes() == 9

# The auto direction should maximize skips.
def test_auto_direction_uniform():
    algorithm, direction = SumRerollIfAnyOnes()._select_algorithm(hdroller.d6.pool(count_dice=[0,1,1,1]))
    assert direction > 0
    algorithm, direction = SumRerollIfAnyOnes()._select_algorithm(hdroller.d6.pool(count_dice=[1,1,1,0]))
    assert direction < 0

# Above that, the auto direction should favor the wide-to-narrow ordering.
def test_auto_direction_max_min_outcomes():
    algorithm, direction = SumRerollIfAnyOnes()._select_algorithm(hdroller.d12.pool(min_outcomes=[8,6,6,6], count_dice=[0,1,1,1]))
    assert direction < 0
    algorithm, direction = SumRerollIfAnyOnes()._select_algorithm(hdroller.d6.pool(max_outcomes=[8,6,6,6], count_dice=[0,1,1,1]))
    assert direction > 0

def sum_dice_func(state, outcome, count):
    return (state or 0) + outcome * count

def test_wrap_func_eval():
    result = hdroller.d6.pool()[0,0,1,1,1].eval(sum_dice_func)
    expected = hdroller.d6.keep_highest(5, 3)
    assert result.equals(expected)

def test_max_outcome_rounding():
    result = hdroller.d12.pool(max_outcomes=[8.5, 8.4, 8.3, 6.1, 6.0]).sum()
    expected = hdroller.d12.pool(max_outcomes=[8, 8, 8, 6, 6]).sum()
    assert result.equals(expected)

def test_min_outcome_rounding():
    result = hdroller.d12.pool(min_outcomes=[8.5, 8.4, 8.3, 6.1, 6.0]).sum()
    expected = hdroller.d12.pool(min_outcomes=[9, 9, 9, 7, 6]).sum()
    assert result.equals(expected)

def test_standard_pool():
    result = hdroller.standard_pool(8, 8, 6, 6, 6).sum()
    expected = 3 @ hdroller.d6 + 2 @ hdroller.d8
    assert result.equals(expected)

def test_runs():
    result = hdroller.FindBestRun()(hdroller.standard_pool(12, 10, 8))
    def func(*outcomes):
        outcomes = sorted(outcomes)
        a = outcomes[1] == outcomes[0] + 1
        b = outcomes[2] == outcomes[1] + 1
        if a and b:
            return 3, outcomes[2]
        elif b:
            return 2, outcomes[2]
        elif a:
            return 2, outcomes[1]
        else:
            return 1, outcomes[2]
    expected = hdroller.apply(func, hdroller.d12, hdroller.d10, hdroller.d8)
    assert result.equals(expected)

class SumFixedDirection(hdroller.EvalPool):
    def __init__(self, direction):
        self._direction = direction

    def next_state(self, state, outcome, count):
        return (state or 0) + outcome * count
    
    def direction(self, *pools):
        return self._direction

test_pools = [
    hdroller.standard_pool(6,6,6),
    hdroller.standard_pool(6,6,6,6)[0,0,0,1],
    hdroller.standard_pool(6,6,6,6)[0,1,1,1],
    hdroller.standard_pool(6,6,6,6)[-1,0,0,1],
    hdroller.standard_pool(12,10,8,8,6,6,6,4),
    hdroller.d12.pool(min_outcomes=[1,2,2,3]),
    hdroller.d12.pool(min_outcomes=[1,2,2,3])[0,0,0,1],
    hdroller.d12.pool(min_outcomes=[1,2,2,3])[1,0,0,0],
    (3 @ hdroller.d6).pool(12)[-6:],
]

eval_ascending = SumFixedDirection(1)
eval_descending = SumFixedDirection(-1)

@pytest.mark.parametrize('pool', test_pools)
def test_sum_direction(pool):
    assert eval_ascending.eval(pool).equals(eval_descending.eval(pool))

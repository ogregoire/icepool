import _context

import hdroller
import pytest

"""
Tests the mix functionality of hdroller.Die() and its derivatives.
"""

def test_mix_d6_faces():
    result = hdroller.Die(1, 2, 3, 4, 5, 6)
    expected = hdroller.d6
    assert result.equals(expected)

def test_mix_identical():
    assert hdroller.Die(hdroller.d6, hdroller.d6, hdroller.d6, hdroller.d6).pmf() == pytest.approx(hdroller.d6.pmf())

def test_mix_weight():
    outcomes = range(2, 13)
    mix_weights = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    result = hdroller.Die(*outcomes, weights=mix_weights)
    expected = 2 @ hdroller.d6
    assert result.equals(expected)
    
def test_mix_mixed():
    die = hdroller.Die(hdroller.d4, hdroller.d6)
    assert die.pmf() == hdroller.Die(weights=[5, 5, 5, 5, 2, 2], min_outcome=1).pmf()

def test_mix_reroll():
    result = hdroller.Die(1,2,3,4,hdroller.Reroll,hdroller.Reroll)
    expected = hdroller.d4
    assert result.equals(expected)

def test_mix_dict_reroll():
    data = {1:1, 2:1, 3:1, 4:1, hdroller.Reroll:10}
    result = hdroller.Die(data, data).reduce()
    expected = hdroller.d4
    assert result.equals(expected)

expected_d6x1 = hdroller.Die(weights=[6, 6, 6, 6, 6, 0, 1, 1, 1, 1, 1, 1], min_outcome=1).trim()

def test_sub_array():
    die = hdroller.d6.sub([5, 4, 1, 2, 3, hdroller.d6 + 6])
    assert die.pmf() == pytest.approx(expected_d6x1.pmf())

def test_sub_dict():
    die = hdroller.d6.sub({6 : hdroller.d6+6})
    assert die.pmf() == pytest.approx(expected_d6x1.pmf())

def test_sub_func():
    die = hdroller.d6.sub(lambda x: hdroller.d6 + 6 if x == 6 else 6 - x)
    assert die.pmf() == pytest.approx(expected_d6x1.pmf())

def test_sub_mix():
    result = hdroller.d6.sub(lambda x: x if x >= 3 else hdroller.Reroll)
    expected = hdroller.d4 + 2
    assert result.equals(expected)

def test_sub_max_depth():
    result = (hdroller.d8 - 1).sub(lambda x: x // 2, max_depth=2).reduce()
    expected = hdroller.d2 - 1
    assert result.equals(expected)

def collatz(x):
    if x == 1:
        return 1
    elif x % 2:
        return x * 3 + 1
    else:
        return x // 2

def test_sub_fixed_point():
    # Collatz conjecture.
    result = hdroller.d100.sub(collatz, max_depth=None).reduce()
    expected = hdroller.Die(1)
    assert result.equals(expected)

"""Submodule containing evaluators."""

__docformat__ = 'google'

from icepool.evaluator.basic import WrapFuncEvaluator, ExpandEvaluator, SumEvaluator, sum_evaluator, CountEvaluator, count_evaluator
from icepool.evaluator.poker import (HighestOutcomeAndCountEvaluator,
                                     LargestCountEvaluator,
                                     LargestCountAndOutcomeEvaluator,
                                     AllCountsEvaluator,
                                     LargestStraightEvaluator,
                                     LargestStraightAndOutcomeEvaluator)
from icepool.evaluator.comparison import (
    ComparisonEvaluator, IsSubsetEvaluator, IsProperSubsetEvaluator,
    IsSupersetEvaluator, IsProperSupersetEvaluator, IsEqualSetEvaluator,
    IsNotEqualSetEvaluator, IsDisjointSetEvaluator)
from icepool.evaluator.joint import JointEvaluator, MapEvaluator

__all__ = [
    'WrapFuncEvaluator', 'ExpandEvaluator', 'SumEvaluator', 'sum_evaluator',
    'CountEvaluator', 'count_evaluator', 'HighestOutcomeAndCountEvaluator',
    'LargestCountEvaluator', 'LargestCountAndOutcomeEvaluator',
    'AllCountsEvaluator', 'LargestStraightEvaluator',
    'LargestStraightAndOutcomeEvaluator', 'ComparisonEvaluator',
    'IsSubsetEvaluator', 'IsProperSubsetEvaluator', 'IsSupersetEvaluator',
    'IsProperSupersetEvaluator', 'IsEqualSetEvaluator',
    'IsNotEqualSetEvaluator', 'IsDisjointSetEvaluator', 'JointEvaluator',
    'MapEvaluator'
]

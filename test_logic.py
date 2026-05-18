import pytest
from calc import calculate_sqrt
from qft_propagator import klein_gordon_propagator_1d
import numpy as np

def test_calculate_sqrt():
    # 正の数
    assert calculate_sqrt(4) == 2.0
    assert calculate_sqrt(9) == 3.0
    # 近似値のテスト
    assert calculate_sqrt(2) == pytest.approx(1.41421356)

def test_klein_gordon_propagator_1d():
    # 距離 0 では相関が 1 になるはず
    assert klein_gordon_propagator_1d(0, 1.0) == 1.0
    
    # 質量が大きいほど減衰が早いはず
    dist = 1.0
    amp_m1 = klein_gordon_propagator_1d(dist, 1.0)
    amp_m2 = klein_gordon_propagator_1d(dist, 2.0)
    assert amp_m1 > amp_m2
    
    # 距離が離れるほど値が小さくなるはず
    assert klein_gordon_propagator_1d(2.0, 1.0) < klein_gordon_propagator_1d(1.0, 1.0)

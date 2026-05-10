import pytest
from parcel_pricer import Parcel, calculate_order

def test_single_small_parcel():
    parcel = Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=1.0)
    result = calculate_order([parcel])
    assert len(result.items) == 1
    assert result.items[0].parcel_type == "Small"
    assert result.items[0].cost == 3.0
    assert result.total_cost == 3.0

def test_single_medium_parcel():
    parcel = Parcel(width=10.0, height=49.9, depth=5.0, weight_kg=1.0)
    result = calculate_order([parcel])
    assert len(result.items) == 1
    assert result.items[0].parcel_type == "Medium"
    assert result.items[0].cost == 8.0
    assert result.total_cost == 8.0

def test_single_large_parcel():
    parcel = Parcel(width=50.0, height=50.0, depth=99.9, weight_kg=1.0)
    result = calculate_order([parcel])
    assert len(result.items) == 1
    assert result.items[0].parcel_type == "Large"
    assert result.items[0].cost == 15.0
    assert result.total_cost == 15.0

def test_single_xl_parcel():
    parcel = Parcel(width=100.0, height=100.0, depth=100.0, weight_kg=1.0)
    result = calculate_order([parcel])
    assert len(result.items) == 1
    assert result.items[0].parcel_type == "XL"
    assert result.items[0].cost == 25.0
    assert result.total_cost == 25.0

def test_boundary_exactly_10_is_medium():
    # If any dimension is 10, it violates "all dimensions < 10"
    parcel = Parcel(width=10.0, height=9.0, depth=9.0, weight_kg=1.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "Medium"
    assert result.items[0].cost == 8.0

def test_boundary_exactly_50_is_large():
    # If any dimension is 50, it violates "all dimensions < 50"
    parcel = Parcel(width=49.0, height=50.0, depth=49.0, weight_kg=1.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "Large"
    assert result.items[0].cost == 15.0

def test_boundary_exactly_100_is_xl():
    # If any dimension is 100, it violates "all dimensions < 100", hence it is XL ("any dimension >= 100cm")
    parcel = Parcel(width=99.0, height=99.0, depth=100.0, weight_kg=1.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "XL"
    assert result.items[0].cost == 25.0

def test_mixed_order():
    parcels = [
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=1.0),      # Small ($3)
        Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=1.0),   # Medium ($8)
        Parcel(width=50.0, height=50.0, depth=50.0, weight_kg=1.0),   # Large ($15)
        Parcel(width=150.0, height=10.0, depth=10.0, weight_kg=1.0)   # XL ($25)
    ]
    result = calculate_order(parcels)
    
    assert len(result.items) == 4
    
    assert result.items[0].parcel_type == "Small"
    assert result.items[1].parcel_type == "Medium"
    assert result.items[2].parcel_type == "Large"
    assert result.items[3].parcel_type == "XL"
    
    assert result.total_cost == 3.0 + 8.0 + 15.0 + 25.0

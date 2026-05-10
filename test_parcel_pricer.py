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

def test_speedy_shipping_off_default():
    parcel = Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=1.0)
    result = calculate_order([parcel])
    assert len(result.items) == 1
    assert result.items[0].parcel_type == "Small"
    assert result.total_cost == 3.0

def test_speedy_shipping_single_parcel():
    parcel = Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=1.0)
    result = calculate_order([parcel], speedy_shipping=True)
    
    assert len(result.items) == 2
    assert result.items[0].parcel_type == "Small"
    assert result.items[0].cost == 3.0
    
    assert result.items[1].parcel_type == "Speedy Shipping"
    assert result.items[1].cost == 3.0
    
    assert result.total_cost == 6.0

def test_speedy_shipping_mixed_order():
    parcels = [
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=1.0),      # Small ($3)
        Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=1.0),   # Medium ($8)
    ]
    result = calculate_order(parcels, speedy_shipping=True)
    
    assert len(result.items) == 3
    
    # Original parcels unchanged
    assert result.items[0].parcel_type == "Small"
    assert result.items[0].cost == 3.0
    
    assert result.items[1].parcel_type == "Medium"
    assert result.items[1].cost == 8.0
    
    # Speedy shipping line item
    assert result.items[2].parcel_type == "Speedy Shipping"
    assert result.items[2].cost == 11.0  # 3.0 + 8.0
    
    # Total doubled
    assert result.total_cost == 22.0

def test_weight_exactly_at_limit_no_surcharge():
    # Medium parcel, weight limit 3kg, actual weight 3kg
    parcel = Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=3.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "Medium"
    assert result.items[0].cost == 8.0  # Base cost $8, no surcharge

def test_weight_1kg_over_limit():
    # Large parcel, weight limit 6kg, actual weight 7.0kg (1kg over)
    # Base cost: $15. Surcharge: 1kg * $2 = $2. Total: $17.
    parcel = Parcel(width=50.0, height=50.0, depth=50.0, weight_kg=7.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "Large"
    assert result.items[0].cost == 17.0

def test_weight_several_kg_over_limit():
    # XL parcel, weight limit 10kg, actual weight 13.9kg (3.9kg over)
    # Rounded down, overweight is 3kg.
    # Base cost: $25. Surcharge: 3kg * $2 = $6. Total: $31.
    parcel = Parcel(width=100.0, height=100.0, depth=100.0, weight_kg=13.9)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "XL"
    assert result.items[0].cost == 31.0

def test_mixed_order_with_weights():
    parcels = [
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=0.5),      # Small ($3, under limit)
        Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=5.5),   # Medium ($8, 2.5kg over -> 2kg * $2 = $4. Total $12)
        Parcel(width=50.0, height=50.0, depth=50.0, weight_kg=6.0),   # Large ($15, exact limit -> $15)
        Parcel(width=150.0, height=10.0, depth=10.0, weight_kg=14.0)  # XL ($25, 4kg over -> 4kg * $2 = $8. Total $33)
    ]
    result = calculate_order(parcels, speedy_shipping=True)
    
    assert len(result.items) == 5
    
    assert result.items[0].cost == 3.0
    assert result.items[1].cost == 12.0
    assert result.items[2].cost == 15.0
    assert result.items[3].cost == 33.0
    
    # Speedy shipping line item
    subtotal = 3.0 + 12.0 + 15.0 + 33.0 # 63.0
    assert result.items[4].parcel_type == "Speedy Shipping"
    assert result.items[4].cost == subtotal
    
    # Total doubled
    assert result.total_cost == subtotal * 2

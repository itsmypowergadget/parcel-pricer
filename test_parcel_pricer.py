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

def test_heavy_cheaper_than_size_based():
    # Small parcel, base $3, weight limit 1kg. Actual weight 30kg.
    # Size cost: 3 + 29*2 = 61.
    # Heavy cost: 50 + 0 = 50.
    # Heavy should be chosen.
    parcel = Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=30.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "Heavy"
    assert result.items[0].cost == 50.0

def test_size_based_cheaper_than_heavy():
    # XL parcel, base $25, limit 10kg. Actual weight 20kg.
    # Size cost: 25 + 10*2 = 45.
    # Heavy cost: 50 + 0 = 50.
    # Size-based should be chosen.
    parcel = Parcel(width=100.0, height=100.0, depth=100.0, weight_kg=20.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "XL"
    assert result.items[0].cost == 45.0

def test_heavy_exactly_50kg_no_surcharge():
    # Small parcel, 50kg.
    # Size cost: 3 + 49*2 = 101.
    # Heavy cost: 50.
    # Heavy should be chosen, exactly $50.
    parcel = Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=50.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "Heavy"
    assert result.items[0].cost == 50.0

def test_heavy_over_50kg():
    # Small parcel, 55kg.
    # Size cost: 3 + 54*2 = 111.
    # Heavy cost: 50 + 5*1 = 55.
    # Heavy should be chosen, cost $55.
    parcel = Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=55.0)
    result = calculate_order([parcel])
    assert result.items[0].parcel_type == "Heavy"
    assert result.items[0].cost == 55.0

def test_mixed_order_heavy_and_size_based():
    parcels = [
        Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=1.0),       # Small, 1kg: Size cost $3, Heavy $50 -> Small $3
        Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=40.0),      # Small, 40kg: Size cost $81, Heavy $50 -> Heavy $50
        Parcel(width=100.0, height=100.0, depth=100.0, weight_kg=15.0) # XL, 15kg: Size cost $35, Heavy $50 -> XL $35
    ]
    result = calculate_order(parcels)
    
    assert len(result.items) == 3
    assert result.items[0].parcel_type == "Small"
    assert result.items[0].cost == 3.0
    
    assert result.items[1].parcel_type == "Heavy"
    assert result.items[1].cost == 50.0
    
    assert result.items[2].parcel_type == "XL"
    assert result.items[2].cost == 35.0
    
    assert result.total_cost == 3.0 + 50.0 + 35.0

def test_discount_4_small_parcels():
    # 4 small parcels, cost $3 each
    parcels = [Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=1.0) for _ in range(4)]
    result = calculate_order(parcels)
    assert len(result.items) == 5 # 4 items + 1 discount
    assert result.items[-1].parcel_type == "Small Mania Discount"
    assert result.items[-1].cost == -3.0
    assert result.total_cost == 12.0 - 3.0

def test_discount_3_medium_parcels():
    # 3 medium parcels, cost $8 each
    parcels = [Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=1.0) for _ in range(3)]
    result = calculate_order(parcels)
    assert len(result.items) == 4
    assert result.items[-1].parcel_type == "Medium Mania Discount"
    assert result.items[-1].cost == -8.0
    assert result.total_cost == 24.0 - 8.0

def test_discount_5_mixed_parcels():
    # 5 different parcels.
    parcels = [
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=1.0),      # Small ($3)
        Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=1.0),   # Medium ($8)
        Parcel(width=50.0, height=50.0, depth=50.0, weight_kg=1.0),   # Large ($15)
        Parcel(width=100.0, height=100.0, depth=100.0, weight_kg=1.0),# XL ($25)
        Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=50.0)      # Heavy ($50)
    ]
    result = calculate_order(parcels)
    assert len(result.items) == 6
    assert result.items[-1].parcel_type == "Mixed Mania Discount"
    assert result.items[-1].cost == -3.0 # The cheapest is the Small ($3)
    assert result.total_cost == 3.0 + 8.0 + 15.0 + 25.0 + 50.0 - 3.0

def test_discount_overlap_small_mixed():
    # 4 expensive Small parcels + 1 cheap Small parcel
    parcels = [
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=24.0), # Small, cost $49
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=24.0), # $49
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=24.0), # $49
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=24.0), # $49
        Parcel(width=1.0, height=1.0, depth=1.0, weight_kg=1.0),  # $3
    ]
    result = calculate_order(parcels)
    assert len(result.items) == 6
    # Choosing Small Mania uses the 4 expensive ones, freeing up $49.
    # Choosing Mixed Mania uses all 5, freeing up the cheapest ($3).
    # Expected is Small Mania.
    assert result.items[-1].parcel_type == "Small Mania Discount"
    assert result.items[-1].cost == -49.0
    
def test_discount_6_medium_parcels():
    # 6 medium parcels ($8 each) -> 2 discounts
    parcels = [Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=1.0) for _ in range(6)]
    result = calculate_order(parcels)
    assert len(result.items) == 8
    discounts = [item for item in result.items if "Discount" in item.parcel_type]
    assert len(discounts) == 2
    assert all(d.parcel_type == "Medium Mania Discount" and d.cost == -8.0 for d in discounts)
    assert result.total_cost == (8.0 * 6) - (8.0 * 2)

def test_speedy_shipping_with_discounts():
    # 3 medium parcels ($8 each) + speedy shipping
    parcels = [Parcel(width=10.0, height=10.0, depth=10.0, weight_kg=1.0) for _ in range(3)]
    result = calculate_order(parcels, speedy_shipping=True)
    assert len(result.items) == 5
    assert result.items[-2].parcel_type == "Medium Mania Discount"
    assert result.items[-2].cost == -8.0
    
    assert result.items[-1].parcel_type == "Speedy Shipping"
    # Subtotal = 24 - 8 = 16. Speedy cost = 16. Total = 32.
    assert result.items[-1].cost == 16.0
    assert result.total_cost == 32.0

def test_specific_overlap_small_and_medium():
    # 4 small parcels (each 5x5x5cm, 0.5kg) = 4 * $3 = $12
    # 1 medium parcel (20x20x20cm, 1kg) = $8
    # User Expects total saving $11 ($9 total)
    parcels = [
        Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=0.5), # Small $3
        Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=0.5), # Small $3
        Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=0.5), # Small $3
        Parcel(width=5.0, height=5.0, depth=5.0, weight_kg=0.5), # Small $3
        Parcel(width=20.0, height=20.0, depth=20.0, weight_kg=1.0) # Medium $8
    ]
    result = calculate_order(parcels)
    assert result.total_cost == 17.0

def test_specific_6_medium_weight_difference():
    # 3 medium parcels (20x20x20cm, 1kg) = $8 each
    # 3 medium parcels (20x20x20cm, 4kg) = $8 + $2 = $10 each
    parcels = [
        Parcel(width=20.0, height=20.0, depth=20.0, weight_kg=1.0), # Medium $8
        Parcel(width=20.0, height=20.0, depth=20.0, weight_kg=1.0), # Medium $8
        Parcel(width=20.0, height=20.0, depth=20.0, weight_kg=1.0), # Medium $8
        Parcel(width=20.0, height=20.0, depth=20.0, weight_kg=4.0), # Medium $10
        Parcel(width=20.0, height=20.0, depth=20.0, weight_kg=4.0), # Medium $10
        Parcel(width=20.0, height=20.0, depth=20.0, weight_kg=4.0)  # Medium $10
    ]
    result = calculate_order(parcels)
    assert result.total_cost == 36.0

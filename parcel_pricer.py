from dataclasses import dataclass
from typing import List

@dataclass
class Parcel:
    width: float
    height: float
    depth: float
    weight_kg: float

@dataclass
class ParcelResult:
    parcel_type: str
    cost: float

@dataclass
class OrderResult:
    items: List[ParcelResult]
    total_cost: float

def calculate_order(parcels: List[Parcel], speedy_shipping: bool = False) -> OrderResult:
    items = []
    total_cost = 0.0
    
    for parcel in parcels:
        max_dim = max(parcel.width, parcel.height, parcel.depth)
        
        if max_dim < 10:
            parcel_type = "Small"
            cost = 3.0
            weight_limit = 1.0
        elif max_dim < 50:
            parcel_type = "Medium"
            cost = 8.0
            weight_limit = 3.0
        elif max_dim < 100:
            parcel_type = "Large"
            cost = 15.0
            weight_limit = 6.0
        else:
            parcel_type = "XL"
            cost = 25.0
            weight_limit = 10.0
            
        overweight = max(0.0, parcel.weight_kg - weight_limit)
        surcharge = int(overweight) * 2.0
        size_cost = cost + surcharge
        
        heavy_overweight = max(0.0, parcel.weight_kg - 50.0)
        heavy_surcharge = int(heavy_overweight) * 1.0
        heavy_cost = 50.0 + heavy_surcharge
        
        if heavy_cost < size_cost:
            cost = heavy_cost
            parcel_type = "Heavy"
        else:
            cost = size_cost
        
        items.append(ParcelResult(parcel_type=parcel_type, cost=cost))
        total_cost += cost
        
    if speedy_shipping:
        items.append(ParcelResult(parcel_type="Speedy Shipping", cost=total_cost))
        total_cost *= 2
        
    return OrderResult(items=items, total_cost=total_cost)

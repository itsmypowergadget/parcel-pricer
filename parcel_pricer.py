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

def calculate_order(parcels: List[Parcel]) -> OrderResult:
    items = []
    total_cost = 0.0
    
    for parcel in parcels:
        max_dim = max(parcel.width, parcel.height, parcel.depth)
        
        if max_dim < 10:
            parcel_type = "Small"
            cost = 3.0
        elif max_dim < 50:
            parcel_type = "Medium"
            cost = 8.0
        elif max_dim < 100:
            parcel_type = "Large"
            cost = 15.0
        else:
            parcel_type = "XL"
            cost = 25.0
            
        items.append(ParcelResult(parcel_type=parcel_type, cost=cost))
        total_cost += cost
        
    return OrderResult(items=items, total_cost=total_cost)

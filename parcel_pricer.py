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

def _calculate_discounts(items: List[ParcelResult]) -> List[ParcelResult]:
    sorted_items = sorted(enumerate(items), key=lambda x: x[1].cost, reverse=True)
    memo = {}

    def solve(idx, s_rem, m_rem, x_rem):
        if idx == len(sorted_items):
            return 0.0, None
        
        state = (idx, s_rem, m_rem, x_rem)
        if state in memo:
            return memo[state]
            
        orig_idx, parcel = sorted_items[idx]
        
        best_val = -1.0
        best_choice = None
        
        # Option 1: Mixed
        nx_rem = (x_rem + 1) % 5
        val_x, _ = solve(idx + 1, s_rem, m_rem, nx_rem)
        if nx_rem == 0:
            val_x += parcel.cost
        if val_x > best_val:
            best_val = val_x
            best_choice = 'X'
            
        # Option 2: Small
        if parcel.parcel_type == "Small":
            ns_rem = (s_rem + 1) % 4
            val_s, _ = solve(idx + 1, ns_rem, m_rem, x_rem)
            if ns_rem == 0:
                val_s += parcel.cost
            if val_s > best_val:
                best_val = val_s
                best_choice = 'S'
                
        # Option 3: Medium
        if parcel.parcel_type == "Medium":
            nm_rem = (m_rem + 1) % 3
            val_m, _ = solve(idx + 1, s_rem, nm_rem, x_rem)
            if nm_rem == 0:
                val_m += parcel.cost
            if val_m > best_val:
                best_val = val_m
                best_choice = 'M'
                
        memo[state] = (best_val, best_choice)
        return memo[state]

    max_val, _ = solve(0, 0, 0, 0)
    
    discounts = []
    if max_val > 0.0:
        s_rem, m_rem, x_rem = 0, 0, 0
        for idx in range(len(sorted_items)):
            state = (idx, s_rem, m_rem, x_rem)
            val, choice = memo[state]
            orig_idx, parcel = sorted_items[idx]
            
            if choice == 'X':
                x_rem = (x_rem + 1) % 5
                if x_rem == 0:
                    discounts.append(ParcelResult(parcel_type="Mixed Mania Discount", cost=-parcel.cost))
            elif choice == 'S':
                s_rem = (s_rem + 1) % 4
                if s_rem == 0:
                    discounts.append(ParcelResult(parcel_type="Small Mania Discount", cost=-parcel.cost))
            elif choice == 'M':
                m_rem = (m_rem + 1) % 3
                if m_rem == 0:
                    discounts.append(ParcelResult(parcel_type="Medium Mania Discount", cost=-parcel.cost))
                    
    return discounts

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
        
    discounts = _calculate_discounts(items)
    for d in discounts:
        items.append(d)
        total_cost += d.cost
        
    if speedy_shipping:
        items.append(ParcelResult(parcel_type="Speedy Shipping", cost=total_cost))
        total_cost *= 2
        
    return OrderResult(items=items, total_cost=total_cost)

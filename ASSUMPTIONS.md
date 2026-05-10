# Assumptions

1. **Dimensional Boundaries:**
   - The requirement "Small: all dimensions < 10cm" implies that if *any* dimension is exactly 10cm or larger, it is no longer small. Therefore, a parcel with dimensions `10x9x9` is classified as "Medium".
   - This same logic is applied to the boundaries of 50cm and 100cm.
   - For XL: "any dimension >= 100cm". This perfectly aligns with our treatment of the boundaries.

2. **Negative and Zero Dimensions:**
   - It is assumed that dimensions and weights will be positive `float` values. Validation for negative or zero dimensions is not currently implemented.

3. **Weight Usage:**
   - `weight_kg` is a required field on the `Parcel` dataclass and is used
     for weight-based surcharge calculations (Step 3 onwards).

4. **Currency:**
   - The cost is represented as a `float` without explicit currency denomination (e.g. `$`). It is assumed the caller will format the value to the appropriate currency.

5. **Future Considerations:**
   - The codebase is structured with clear iterations through the parcels.
     Weight surcharges, speedy shipping, and discounts are implemented as
     separate, composable operations on the order rather than monolithic logic.
     This makes it straightforward to add or modify pricing rules independently.

6. **Weight Surcharges:**
   - Weight surcharge is calculated on whole kg over the limit, rounded down
     (e.g. 1.9kg over = 1kg surcharge, not 2kg).
   - Parcels exactly at the weight limit incur no surcharge.
   - Surcharge applies based on the parcel's size classification, not its weight.

7. **Heavy Parcels:**
   - Similar to weight surcharges, the per-kg penalty over 50kg for Heavy parcels rounds down to the nearest whole kg.
   - When the size-based cost and the Heavy cost are exactly equal, the size-based classification is preferred to maintain specificity (e.g. an XL parcel with 10kg limit vs 50kg limit).

8. **Discounts:**
   - A single parcel can only belong to one discount group.
   - Within each discount group, the cheapest parcel in that group is treated as the free one, maximising savings.
   - The combination of discount groups that yields the greatest total saving is always selected.
   - If two combinations yield the same total saving, either may be selected.
   - Discounts are listed as separate negative line items in the output and do not mutate individual parcel costs.
   - Speedy shipping is applied after discounts, doubling the post-discount total.
# Assumptions

1. **Dimensional Boundaries:**
   - The requirement "Small: all dimensions < 10cm" implies that if *any* dimension is exactly 10cm or larger, it is no longer small. Therefore, a parcel with dimensions `10x9x9` is classified as "Medium".
   - This same logic is applied to the boundaries of 50cm and 100cm.
   - For XL: "any dimension >= 100cm". This perfectly aligns with our treatment of the boundaries.

2. **Negative and Zero Dimensions:**
   - It is assumed that dimensions and weights will be positive `float` values. Validation for negative or zero dimensions is not currently implemented in this step.

3. **Weight Usage:**
   - `weight_kg` is currently a required field on the `Parcel` dataclass but does not yet affect pricing. It's in place for future weight-based surcharges.

4. **Currency:**
   - The cost is represented as a `float` without explicit currency denomination (e.g. `$`). It is assumed the caller will format the value to the appropriate currency.

5. **Future Considerations:**
   - The codebase is structured with clear iterations through the parcels. Extending `calculate_order` to support weight-based surcharges or speedy shipping can easily be added as subsequent operations or parameters. Discounter modules could also act upon the resulting `OrderResult`.
